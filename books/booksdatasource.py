#!/usr/bin/env python3
#Written by Lysander Miller and Thea Traw
#Revised by Lysander Miller
'''
    booksdatasource.py
    Jeff Ondich, 21 September 2021

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
'''

import csv

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

class BooksDataSource:
    def __init__(self, books_csv_file_name):
        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        self.list_of_authors = []
        self.list_of_books = []
        books_file = open(books_csv_file_name, 'r')
        books_file_reader = csv.reader(books_file)
        two_authors = False
        for row in books_file_reader:
            title = row[0]
            publication_year = row[1]
            author_and_years = [row[2]]
            if 'and' in author_and_years[0]:
                first_author_index = 0
                second_author_index = 1
                split_two_authors = author_and_years[0].split('and')
                split_two_authors[first_author_index] = split_two_authors[0][:-1]
                split_two_authors[second_author_index] = split_two_authors[1][1:]
                author_and_years[0] = split_two_authors[first_author_index]
                author_and_years.append(split_two_authors[second_author_index])
                two_authors = True
            for author in author_and_years:
                authors_first_name = author.split(' ')[0]
                authors_last_name = ''
                authors_birth_year = None
                authors_death_year = None
                if len(author.split(' ')) > 3:
                    authors_last_name = author.split(' ')[2]
                else:
                    authors_last_name = author.split(' ')[1]
                if author[-2:][0] == '-':
                    authors_birth_year = author[-6:][:4]
                else:
                    authors_birth_year = author[-10:][:4]
                    authors_death_year = author[-5:][:4]
                my_author = Author(authors_last_name, authors_first_name, authors_birth_year, authors_death_year)
                if (my_author in self.list_of_authors) == False:
                    self.list_of_authors.append(my_author)
            if two_authors == True:
                list_to_pass = [self.list_of_authors[(len(self.list_of_authors)-1)], self.list_of_authors[len(self.list_of_authors)-2]]
                self.list_of_books.append(Book(title, publication_year, list_to_pass))
            else:
                list_to_pass = [self.list_of_authors[(len(self.list_of_authors)-1)]]
                self.list_of_books.append(Book(title, publication_year, list_to_pass))
            two_authors = False

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        list_of_authors_with_this_string = []
        if search_text == None:
            list_of_authors_sorted = sorted(self.list_of_authors, key=lambda x: x.surname)
            return list_of_authors_sorted
        else:
            search_text = search_text.lower()
            for author in self.list_of_authors:
                if (search_text in author.surname.lower()) or (search_text in author.given_name.lower()):
                    list_of_authors_with_this_string.append(author)
            list_of_authors_with_this_string = sorted(list_of_authors_with_this_string, key=lambda x: (x.surname, x.given_name))
            return list_of_authors_with_this_string

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''

        selected_books = []

        if search_text == None:
            selected_books = self.list_of_books

        else:
            for book in self.list_of_books:
                if search_text.casefold() in book.title.casefold():
                    selected_books.append(book)

        if sort_by != 'year' or sort_by == 'title':
            return sorted(selected_books, key=lambda book: (book.title))

        else:
            return sorted(selected_books, key=lambda book: (book.publication_year, book.title))


    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''

        start_year_none = False
        end_year_none = False

        if start_year == 'None' or start_year == None:
            start_year_none = True
        if end_year == 'None' or end_year == None:
            end_year_none = True

        try:
            
            if start_year_none == False: 
                x = int(start_year)
            if end_year_none == False:
                y = int(end_year)
        except ValueError:
            raise ValueError('sorry, invalid input') from None
            quit()

        selected_books = []

        if start_year_none == True and end_year_none == True: 
            selected_books = self.list_of_books
            
        elif start_year_none == True:
            for book in self.list_of_books:
                if int(book.publication_year) <= int(end_year):
                    selected_books.append(book)

        elif end_year_none == True:
            for book in self.list_of_books:
                if int(book.publication_year) >= int(start_year):
                    selected_books.append(book)

        else: #neither term is None
            
            for book in self.list_of_books:
                if int(book.publication_year) >= int(start_year) and int(book.publication_year) <= int(end_year):
                    selected_books.append(book)
                    
        return sorted(selected_books, key=lambda book: (book.publication_year, book.title))

