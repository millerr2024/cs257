#This is code by Thea Traw and Lysander Miller
#Revised by Lysander Miller
from booksdatasource import Book, Author, BooksDataSource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = BooksDataSource('books1.csv')
    def tearDown(self):
        pass
    def test_unique_author(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Pratchett', 'Terry'))
    def test_a_noneCase(self):
        self.smaller_data_source = BooksDataSource('testNone.csv')
        what_should_be_returned = [Author('Brontë', 'Charlotte'),Author('Márquez', 'Gabriel'),Author('Wodehouse', 'Pelham')]
        self.assertEqual(self.smaller_data_source.authors(None), what_should_be_returned)
    def test_a_alphabeticallyBySurname(self):
        self.smaller_data_source = BooksDataSource('a_alphabeticallyBySurname.csv')
        what_should_be_returned = [Author('Dunnewold', 'Mary'),Author('Hosseini', 'Khaled'),Author('Sterne', 'Laurence')]
        self.assertEqual(self.smaller_data_source.authors('a'), what_should_be_returned)
    def test_a_alphabeticallyByFirstName(self):
        self.smaller_data_source = BooksDataSource('a_alphabeticallyByFirstName.csv')
        what_should_be_returned = [Author('Brontë','Ann'),Author('Brontë','Charlotte'),Author('Brontë','Emily')]
        self.assertEqual(self.smaller_data_source.authors('Brontë'), what_should_be_returned)
    def test_a_testTwoAuthors(self):
        what_should_be_returned = [Author('Gaiman', 'Neil'),Author('Pratchett','Terry')]
        list_one = self.data_source.authors('Pratchett')
        list_two = self.data_source.authors('Gaiman')
        list_three = list_one + list_two
        list_three = sorted(list_three, key=lambda x: (x.surname, x.given_name))
        self.assertEqual(list_three, what_should_be_returned)
    def test_a_typoTest(self):
        self.assertEqual(self.data_source.authors('f1re'), [])
        
    def test_t_typoTest(self):
        self.assertEqual(self.data_source.books('f1re'), [])
    def test_t_defaultTest(self):
        what_should_be_returned = [Book('Omoo', 1847, [Author('Melville', 'Herman')])]
        self.assertEqual(self.data_source.books('Omoo'), what_should_be_returned)
    def test_t_noneTest(self):
        self.smaller_data_source = BooksDataSource('testNone.csv')
        what_should_be_returned = [Book('Jane Eyre', 1847, [Author('Brontë', 'Charlotte')]),Book('Leave it to Psmith', 1923, [Author('Wodehouse', 'Pelham Grenville')]),Book('Love in the Time of Cholera', 1985, [Author('García Márquez', 'Gabriel')])]
        self.assertEqual(self.smaller_data_source.books(None), what_should_be_returned)
    def test_t_portionTest(self):
        what_should_be_returned = [Book('Wuthering Heights', 1847, [Author('Brontë', 'Emily')])]
        self.assertEqual(self.data_source.books('Wu'), what_should_be_returned)
    def test_t_alphabeticalByTitle(self):
        self.assertEqual(self.data_source.books('time', 'title'), [Book('Love in the Time of Cholera', 1985, [Author('García Márquez', 'Gabriel')]), Book('The Fire Next Time', 1963, [Author('Baldwin', 'James')]), Book('Thief of Time', 1996, [Author('Pratchett', 'Terry')])])
    def test_t_sortByYear(self):
        self.assertEqual(self.data_source.books('time', 'year'), [Book('The Fire Next Time', 1963, [Author('Baldwin', 'James')]), Book('Love in the Time of Cholera', 1985, [Author('García Márquez', 'Gabriel')]), Book('Thief of Time', 1996, [Author('Pratchett', 'Terry')])])

    def test_y_typoTest(self):
        self.assertRaises(ValueError, self.data_source.books_between_years, 2000, 'hello')
    def test_y_startYearNone(self):
        self.assertEqual(self.data_source.books_between_years(None, 1815), [Book('The Life and Opinions of Tristram Shandy, Gentleman', 1759, [Author('Sterne', 'Laurence')]), Book('Pride and Prejudice', 1813, [Author('Austen', 'Jane')]), Book('Sense and Sensibility', 1813, [Author('Austen', 'Jane')]), Book('Emma', 1815, [Author('Austen', 'Jane')])])
    def test_y_endYearNone(self):
        self.assertEqual(self.data_source.books_between_years(2019, None), [Book('Fine, Thanks', 2019, [Author('Dunnewold', 'Mary')]), Book('Boys and Sex', 2020, [Author('Orenstein', 'Peggy')]), Book('The Invisible Life of Addie LaRue', 2020, [Author('Schwab', 'V.E.')])])
    def test_y_doubleNoneTest(self):
        self.smaller_data_source = BooksDataSource('testNone.csv')
        what_should_be_returned = [Book('Jane Eyre', 1847, [Author('Brontë', 'Charlotte')]),Book('Leave it to Psmith', 1923, [Author('Wodehouse', 'Pelham Grenville')]),Book('Love in the Time of Cholera', 1985, [Author('García Márquez', 'Gabriel')])]
        self.assertEqual(self.smaller_data_source.books_between_years(None, None), what_should_be_returned)
    def test_y_inclusiveAndTieBreaker(self):
        self.assertEqual(self.data_source.books_between_years(2005, 2010), [Book('1Q84', 2009, [Author('Murakami', 'Haruki')]), Book('All Clear', 2010, [Author('Willis', 'Connie')]), Book('Blackout', 2010, [Author('Willis', 'Connie')])])

if __name__ == '__main__':
    unittest.main()
