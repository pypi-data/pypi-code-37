def mount(role_arn, bucket_path, mount_path):
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
        print("already mounted")