from pyspark.sql.types import *
from optimus import Optimus
from pyspark.ml.linalg import Vectors, VectorUDT, DenseVector
import numpy as np

nan = np.nan
import datetime
from pyspark.sql import functions as F

op = Optimus(master='local')
source_df = op.create.df(
    [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
     ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
     ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
     ('date arrival', StringType(), True), ('last date seen', StringType(), True),
     ('attributes', ArrayType(FloatType(), True), True), ('DateType', DateType(), True),
     ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
     ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", 28, 'Leader', 10, 5000000,
                                                                                  4.300000190734863,
                                                                                  ['Inochi', 'Convoy'],
                                                                                  '19.442735,-99.201111', '1980/04/10',
                                                                                  '2016/09/10',
                                                                                  [8.53439998626709, 4300.0],
                                                                                  datetime.date(2016, 9, 10),
                                                                                  datetime.datetime(2014, 6, 24, 0, 0),
                                                                                  True, bytearray(b'Leader'), None), (
                                                                                     'bumbl#ebéé  ', 17, 'Espionage', 7,
                                                                                     5000000, 2.0,
                                                                                     ['Bumble', 'Goldback'],
                                                                                     '10.642707,-71.612534',
                                                                                     '1980/04/10',
                                                                                     '2015/08/10',
                                                                                     [5.334000110626221, 2000.0],
                                                                                     datetime.date(2015, 8, 10),
                                                                                     datetime.datetime(2014, 6, 24, 0,
                                                                                                       0),
                                                                                     True, bytearray(b'Espionage'),
                                                                                     None), (
                                                                                     'ironhide&', 26, 'Security', 7,
                                                                                     5000000, 4.0, ['Roadbuster'],
                                                                                     '37.789563,-122.400356',
                                                                                     '1980/04/10',
                                                                                     '2014/07/10',
                                                                                     [7.924799919128418, 4000.0],
                                                                                     datetime.date(2014, 6, 24),
                                                                                     datetime.datetime(2014, 6, 24, 0,
                                                                                                       0),
                                                                                     True, bytearray(b'Security'),
                                                                                     None), (
                                                                                     'Jazz', 13, 'First Lieutenant', 8,
                                                                                     5000000, 1.7999999523162842,
                                                                                     ['Meister'],
                                                                                     '33.670666,-117.841553',
                                                                                     '1980/04/10', '2013/06/10',
                                                                                     [3.962399959564209, 1800.0],
                                                                                     datetime.date(2013, 6, 24),
                                                                                     datetime.datetime(2014, 6, 24, 0,
                                                                                                       0),
                                                                                     True,
                                                                                     bytearray(b'First Lieutenant'),
                                                                                     None), (
                                                                                     'Megatron', None, 'None', 10,
                                                                                     5000000,
                                                                                     5.699999809265137, ['Megatron'],
                                                                                     None,
                                                                                     '1980/04/10', '2012/05/10',
                                                                                     [None, 5700.0],
                                                                                     datetime.date(2012, 5, 10),
                                                                                     datetime.datetime(2014, 6, 24, 0,
                                                                                                       0),
                                                                                     True, bytearray(b'None'), None), (
                                                                                     'Metroplex_)^$', 300,
                                                                                     'Battle Station',
                                                                                     8, 5000000, None, ['Metroflex'],
                                                                                     None,
                                                                                     '1980/04/10', '2011/04/10',
                                                                                     [91.44000244140625, None],
                                                                                     datetime.date(2011, 4, 10),
                                                                                     datetime.datetime(2014, 6, 24, 0,
                                                                                                       0),
                                                                                     True, bytearray(b'Battle Station'),
                                                                                     None)])


class Testdf_sql(object):
    @staticmethod
    def test_query():
        source_df.table_name('temp_name')
        actual_df = source_df.query('SELECT * FROM temp_name')
        expected_value = source_df
        assert (expected_value.collect() == actual_df.collect())