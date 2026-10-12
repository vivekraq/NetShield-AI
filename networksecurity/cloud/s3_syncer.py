class S3Sync:
    def sync_folder_to_s3(self, folder, aws_bucket_url):
        raise NotImplementedError(
            "S3 synchronization is not configured yet. "
            "Configure AWS S3 before running the training pipeline."
        )
