from .everything import check_everything
from .lint import check_lint
from .news import check_news

COMMANDS = {
    'everything': check_everything,
    'lint': check_lint,
    'news': check_news
}
