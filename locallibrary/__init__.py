def index(request):
    # Основная статистика
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    # Для курсовой - расширенная аналитика
    from django.db.models import Count, Avg
    from datetime import datetime, timedelta

    # Книги, добавленные за последний месяц
    last_month = datetime.now() - timedelta(days=30)
    recent_books_count = Book.objects.filter(
        created_date__gte=last_month
    ).count()

    # Среднее количество экземпляров на книгу
    avg_copies_per_book = BookInstance.objects.values('book').annotate(
        count=Count('id')
    ).aggregate(avg=Avg('count'))['avg'] or 0

    # Самые популярные авторы (по количеству книг)
    popular_authors = Author.objects.annotate(
        book_count=Count('book')
    ).order_by('-book_count')[:3]

    # Счетчик посещений с временем последнего визита
    session_data = {
        'num_visits': request.session.get('num_visits', 0),
        'last_visit': request.session.get('last_visit')
    }

    request.session['num_visits'] = session_data['num_visits'] + 1
    request.session['last_visit'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': ['num_visits'],
        'last_visit': session_data['last_visit'],
        'recent_books_count': recent_books_count,
        'avg_copies_per_book': round(avg_copies_per_book, 1),
        'popular_authors': popular_authors,
    }

    return render(request, 'index.html', context=context)