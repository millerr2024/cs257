#This is code by Lysander Miller and Thea Traw
#Revised by Lysander Miller

import argparse
import booksdatasource
import csv

#This section sets up the argument parser
def get_parsed_arguments():
        parser = argparse.ArgumentParser(description='Sorts books and authors')
        parser.add_argument('--titles', '-t', nargs='*',default='NoData', help='sort by titles')
        parser.add_argument('--authors', '-a',nargs='*',default='NoData',  help='sort by authors')
        parser.add_argument('--years', '-y',nargs='*',default='NoData', help='sort by years')
        parser.add_argument('--moreHelp', '-mh', '-mH', nargs='*', default = 'NoData', help='provides more information on search')
        parsed_arguments = parser.parse_args()
        return parsed_arguments

def main():
    initialized_books_data_source = booksdatasource.BooksDataSource('books1.csv')
    arguments = get_parsed_arguments()
    list_of_authors = []
    list_of_authors_already_printed = []
    #Code for the moreHelp flag
    if arguments.moreHelp != 'NoData':
        file = open('usage.txt', 'r')
        contents = file.read()
        print(contents)
    #Code for the authors flag
    if arguments.authors != 'NoData':
        if (len(arguments.authors)) > 0:
            for author_string in arguments.authors:
                list_of_authors += initialized_books_data_source.authors(author_string)
        elif (len(arguments.authors)) == 0:
            list_of_authors = initialized_books_data_source.authors(None)
        list_of_authors = sorted(list_of_authors, key=lambda x: (x.surname, x.given_name))
        for author in list_of_authors:
            if (author in list_of_authors_already_printed) == False:
                print(author.surname+', '+author.given_name)
                list_of_authors_already_printed.append(author)
    #Code for the titles flag
    if arguments.titles != 'NoData':
        sorted_by_year = False
        list_of_books = []
        index = 0
        if (len(arguments.titles) == 0):
            list_of_books = initialized_books_data_source.books(None, 'title')
        else:
            for title in arguments.titles:
                if title == 'year':
                    sorted_by_year = True
                    index +=1
                elif title == 'title':
                    index +=1
                    pass
                else:
                    if sorted_by_year == True:
                        list_of_books += initialized_books_data_source.books(title, 'year')
                    else:
                        list_of_books += initialized_books_data_source.books(title, 'title')
                if (len(arguments.titles)) == index:
                    if sorted_by_year == True:
                        list_of_books = initialized_books_data_source.books(None, 'year')
                    else:
                        list_of_books = initialized_books_data_source.books(None, 'title')
            if sorted_by_year == False:
                list_of_books = sorted(list_of_books, key=lambda x: (x.title))
            else:
                list_of_books = sorted(list_of_books, key=lambda x: (x.publication_year, x.title))
        list_of_books_already_printed = []
        for book in list_of_books:
            if book not in list_of_books_already_printed:
                print(book.title)
                list_of_books_already_printed.append(book)
    #Code for the years flag
    if arguments.years != 'NoData':
        if len(arguments.years) == 0:
            list_of_books = initialized_books_data_source.books_between_years(None, None)
            for book in list_of_books:
                print(book.title)
        elif len(arguments.years) > 2:
            print('You have entered too many arguments')
        else:
            first_year_index = 0
            second_year_index = 1
            if len(arguments.years) == 1:
                list_of_books = initialized_books_data_source.books_between_years(arguments.years[first_year_index], None)
            elif arguments.years[first_year_index].lower() == 'none' and arguments.years[second_year_index].lower() != 'none':
                list_of_books = initialized_books_data_source.books_between_years(None, arguments.years[second_year_index])
            elif arguments.years[second_year_index].lower() == 'none' and arguments.years[first_year_index].lower() != 'none':
                list_of_books = initialized_books_data_source.books_between_years(arguments.years[first_year_index], None)
            elif arguments.years[first_year_index].lower() == 'none' and arguments.years[second_year_index].lower() == 'none':
                list_of_books = initialized_books_data_source.books_between_years(None, None)
            else:
                list_of_books = initialized_books_data_source.books_between_years(arguments.years[first_year_index], arguments.years[second_year_index])
            for book in list_of_books:
                print(book.title)
#Main function
if __name__ == '__main__':
    main()
