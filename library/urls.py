from rest_framework.routers import DefaultRouter
from .views.library_user import LibraryUserListApiView
from .views.book import BookListApiView
from .views.book_item import BookItemListApiView

router = DefaultRouter()
add_to_router = router.register

add_to_router("users", LibraryUserListApiView)

add_to_router('books', BookListApiView)
add_to_router('books_by', BookListApiView.BookByListApiView)

add_to_router('book_items', BookItemListApiView) 


urlpatterns = router.urls