from pyspark import SparkContext

def get_dbutils(spark):
    try:
        from pyspark.dbutils import DBUtils
        dbutils = DBUtils(spark)
    except ImportError:
        import IPython
        dbutils = IPython.get_ipython().user_ns["dbutils"]
    return dbutils


def mount(role_arn, bucket_path, mount_path, sc = None, dbutils = None):
    if sc is None:
        sc = SparkContext.getOrCreate()
    if dbutils is None:
        dbutils = get_dbutils(sc)

    try:
       sc._jsc.hadoopConfiguration().set("fs.s3a.credentialsType", "AssumeRole")
       sc._jsc.hadoopConfiguration().set("fs.s3a.stsAssumeRole.arn", role_arn)
       print(sc._jsc.hadoopConfiguration().get("fs.s3a.stsAssumeRole.arn") == role_arn)
       dbutils.fs.mount(
            "s3a://{}".format(bucket_path),
            mount_path,
            extra_configs = {
                "fs.s3a.credentialsType" : "AssumeRole",
                "fs.s3a.stsAssumeRole.arn" : role_arn
            }
       )
    except:
       print("Error:- already mounted or invalid role")
