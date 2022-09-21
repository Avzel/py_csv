import os
import unittest
from py_csv.csv_parser import CSVParser
from py_csv.exceptions import CSVParseException


class TestCSVParser(unittest.TestCase):

    def setUp(self) -> None:

        with open('valid1.csv', 'w') as file:
            file.writelines([
                'name,age\n',
                'Alice,0\n',
                'Bob,1\n',
                ])

        with open('valid2.csv', 'w') as file:
            file.writelines([
                'from,to,num,msg\n',
                'Alice,Bob,1,"Hello!"\n',
                'Bob,Alice,2,"Hello to you too!"\n',
                'Alice,Bob,3,"do you like newlines?\n',
                'like this?"\n',
                'Bob,Alice,4,"Nope."',
                ])

        with open('valid3.csv', 'w') as file:
            file.writelines([
                'from,to,num,msg\n',
                'Alice,Bob,5,"Remember when I said ""Hello!""?"\n',
                'Bob,Alice,6,"Yeah, I remember"'
                ])

        with open('valid4.csv', 'w') as file:
            file.writelines([
            '"dq and comma","new line","empty field",0,"combination of stuff"\n',
            '""",","\n',
            '",,"0",""",""""\n',
            '123""""""""|*~\/<>.?-+=_^@,qwe,$%#$,\n',
            ',\n',
            ',rty\n',
            '"""',
                ])

        with open('invalid1.csv', 'w') as file:
            file.writelines([
                'header1,header2,header3\n',
                'field"1",field"2",field"3"',
                ])

        with open('invalid2.csv', 'w') as file:
            file.writelines([
                'header1,header2,header3\n',
                '"field"1"","field"2"","field"3""',
                ])

        with open('invalid3.csv', 'w') as file:
            file.writelines([
                'header1,header2,header3\n',
                'field1,field2,field3,field4'
                ])

    def tearDown(self) -> None:

        os.remove('valid1.csv')
        os.remove('valid2.csv')
        os.remove('valid3.csv')
        os.remove('valid4.csv')
        os.remove('invalid1.csv')
        os.remove('invalid2.csv')
        os.remove('invalid3.csv')

    def test_set_file(self) -> None:

        parser1 = CSVParser('valid1.csv')
        self.assertEqual(parser1._CSVParser__file.name, 'valid1.csv')
        parser1._CSVParser__file.close()

        parser2 = CSVParser()
        parser2.set_file('valid2.csv')
        self.assertEqual(parser2._CSVParser__file.name, 'valid2.csv')
        parser2._CSVParser__file.close()

    def test_valid_read_row(self) -> None:

        parser = CSVParser('valid1.csv')
        self.assertEqual(parser.read_row(), {'name': 'Alice', 'age': '0'})
        self.assertEqual(parser.read_row(), {'name': 'Bob', 'age': '1'})
        self.assertIsNone(parser.read_row())
        parser._CSVParser__file.close()

        parser = CSVParser('valid2.csv')
        self.assertEqual(parser.read_row(), 
            {'from': 'Alice', 'to': 'Bob', 'num': '1', 'msg': 'Hello!'})
        self.assertEqual(parser.read_row(), 
            {'from': 'Bob', 'to': 'Alice', 'num': '2', 'msg': 'Hello to you too!'})
        self.assertEqual(parser.read_row(), 
            {'from': 'Alice', 'to': 'Bob', 'num': '3', 'msg': 'do you like newlines?\nlike this?'})
        self.assertEqual(parser.read_row(), 
            {'from': 'Bob', 'to': 'Alice', 'num': '4', 'msg': 'Nope.'})
        self.assertIsNone(parser.read_row())
        parser._CSVParser__file.close()

        parser = CSVParser('valid3.csv')
        self.assertEqual(parser.read_row(), 
            {'from': 'Alice', 'to': 'Bob', 'num': '5', 'msg': 'Remember when I said "Hello!"?'})
        self.assertEqual(parser.read_row(), 
            {'from': 'Bob', 'to': 'Alice', 'num': '6', 'msg': 'Yeah, I remember'})
        self.assertIsNone(parser.read_row())
        parser._CSVParser__file.close()

        parser = CSVParser('valid4.csv')
        self.assertEqual(parser.read_row(),
            {
            'dq and comma': '",', 
            'new line': '\n', 
            'empty field': '', 
            '0': '0', 
            'combination of stuff': 
                '",""\n123""""|*~\/<>.?-+=_^@,qwe,$%#$,\n,\n,rty\n"'
            })
        self.assertIsNone(parser.read_row())
        parser._CSVParser__file.close()

    def test_invalid_read_row(self) -> None:

        parser = CSVParser('invalid1.csv')
        try:
            parser.read_row()
            self.assertFalse(True)
        except CSVParseException as e:
            self.assertEqual(e.column, 6)
            self.assertEqual(e.line, 2)
            self.assertEqual(e.row, 2)
            self.assertEqual(e.field, 1)
        parser._CSVParser__file.close()

        parser = CSVParser('invalid2.csv')
        try:
            parser.read_row()
            self.assertFalse(True)
        except CSVParseException as e:
            self.assertEqual(e.column, 8)
            self.assertEqual(e.line, 2)
            self.assertEqual(e.row, 2)
            self.assertEqual(e.field, 1)
        parser._CSVParser__file.close()

        parser = CSVParser('invalid3.csv')
        try:
            parser.read_row()
            self.assertFalse(True)
        except CSVParseException as e:
            self.assertEqual(e.column, 22)
            self.assertEqual(e.line, 2)
            self.assertEqual(e.row, 2)
            self.assertEqual(e.field, 4)
        parser._CSVParser__file.close()

    def test_reset(self) -> None:

        parser = CSVParser('valid1.csv')
        parser.reset()
        self.assertTrue(parser._CSVParser__file.closed)

if __name__ == '__main__':
    unittest.main()
