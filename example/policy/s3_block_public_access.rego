package rules.aws.s3

__rego__metadoc__ := {
    "id": "PL159",
    "title": "S3 bucket should not be exposed to the internet",
    "description": "S3 buckets should have all `block public access` options enabled.",
    "custom": {
        "severity": "High",
        "controls": "CIS-AWS_v1.3.0"
    }
}