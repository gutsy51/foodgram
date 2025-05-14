from django.contrib.admin import SimpleListFilter
from django.db.models import Avg


class AbstractNumberFilter(SimpleListFilter):
    """Base class for count filters.

    Basically, provides filters:
    - Empty (0)
    - Not empty (>0)
    - A little (<N)
    - Medium (>N && <M)
    - A lot (>M)
    where N and M are calculated as:
        N = average_count * 0.75
        M = average_count * 1.25

    Also, in the URL you can specify your own value in the format of the type:
        /?parameter_name=>X
        /?parameter_name=<X
        /?parameter_name=X
    where X is a number.
    You can also separate several values with a comma, for example:
        /?parameter_name=>2,<5
    will return values in range (2,5).

    To make custom filters, override the `_get_lookups` method.
    """

    title = None
    parameter_name = None

    @staticmethod
    def _get_lookups(n, m):
        return [
            ('0', 'Нет'),
            ('>0', 'Есть'),
            (f'<{n}', f'Мало - меньше {n}'),
            (f'>{n - 1},<{m + 1}', f'Средне - от {n} до {m}'),
            (f'>{m}', f'Много - больше {m}'),
        ]

    def lookups(self, request, model_admin):
        queryset = model_admin.get_queryset(request)
        avg = queryset.aggregate(avg=Avg(self.parameter_name))['avg'] or 1
        n = int(avg * 0.75) or 1  # Set 1 and 2 if avg is 0.
        m = int(avg * 1.25) if n > 1 else 2
        return self._get_lookups(n, m)

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        filters = {}
        for part in value.split(','):
            try:
                if part.startswith('>'):
                    filters[f'{self.parameter_name}__gt'] = int(part[1:])
                elif part.startswith('<'):
                    filters[f'{self.parameter_name}__lt'] = int(part[1:])
                elif part.isdigit():
                    filters[self.parameter_name] = int(part)
            except ValueError:
                continue  # Ignore invalid values.
        return queryset.filter(**filters)


class RecipeCountFilter(AbstractNumberFilter):
    title = 'Рецепты'
    parameter_name = 'recipe_count'


class SubscriptionCountFilter(AbstractNumberFilter):
    title = 'Подписки'
    parameter_name = 'subscriptions_count'


class SubscriberCountFilter(AbstractNumberFilter):
    title = 'Подписчики'
    parameter_name = 'subscribers_count'


class UsedInRecipesCountFilter(AbstractNumberFilter):
    title = 'Использован в рецептах'
    parameter_name = 'used_in_recipes_count'


class CookingTimeFilter(AbstractNumberFilter):
    title = 'Время приготовления'
    parameter_name = 'cooking_time'

    @staticmethod
    def _get_lookups(n, m):
        return [
            (f'<{n}', f'Быстро - быстрее {n} минут'),
            (f'>{n - 1},<{m + 1}', f'Средне - от {n} до {m} минут'),
            (f'>{m}', f'Долго - дольше {m} минут'),
        ]
