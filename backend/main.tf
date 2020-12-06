provider "aws" {
  region = "us-east-1"
  access_key=""
  secret_key=""

}

resource "aws_security_group" "ec2-elb-sg" {
  name = "ec2-elb-sg"

  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 6379
    to_port = 6379
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "oauth-sg" {
  name = "oauth-sg"

  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 8000
    to_port = 8000
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 8001
    to_port = 8001
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "admin-sg" {
  name = "admin-sg"

  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0", "::/0"]
  }

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0", "::/0"]
  }

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0", "::/0"]
  }

  ingress {
    from_port = 8000
    to_port = 9000
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0", "::/0"]
  }

}

resource "aws_db_instance" "default" {
  allocated_storage    = 20
  storage_type         = "ssd"
  engine               = "postgresql"
  engine_version       = "12.3"
  instance_class       = "db.t2.micro"
  name                 = "mydb"
  username             = "postgres"
  password             = "postgres"
  parameter_group_name = "default.postgres12"
  db_subnet_group_name = aws_db_subnet_group.default.name
}

resource "aws_db_subnet_group" "default" {
  name       = "main"
  subnet_ids = ["subnet-b647f3e9", "subnet-c849b6f9", "subnet-68f34249", "subnet-47d6ad0a", "subnet-3795f839", "subnet-a09d36c6"]

  tags = {
    Name = "My DB subnet group"
  }
}

# resource "aws_key_pair" "default" {
#   key_name = "ec2-elb-key"
#   public_key = "${file("/root/.ssh/id_rsa.pub")}"
# }

resource "aws_launch_template" "foobar" {
  name_prefix   = "testing"
  image_id      = "ami-0626d971317455809"
  instance_type = "t2.micro"
}

resource "aws_autoscaling_group" "bar" {
  availability_zones = ["us-east-1a", "us-east-1c"]
  desired_capacity   = 2
  max_size           = 3
  min_size           = 1
  load_balancers = [ "value" ]

  launch_template {
    id      = aws_launch_template.foobar.id
    version = "$Latest"
  }
}


resource "aws_instance" "oauth" {
  ami = "ami-0dba2cb6798deb6d8"
  instance_type = "t2.micro"
  #key_name = "${aws_key_pair.default.id}"
  security_groups = ["${aws_security_group.oauth-sg.name}"]
  # user_data = "${file("bootstrap-server2.sh")}"
}

resource "aws_instance" "admin" {
  ami = "ami-00ddb0e5626798373"
  instance_type = "t2.micro"
  # key_name = "${aws_key_pair.default.id}"
  security_groups = ["${aws_security_group.admin-sg.name}"]
  # user_data = "${file("bootstrap-server2.sh")}"
}

resource "aws_elb" "default" {
  name = "ec2-elb"
  # instances = ["${aws_instance.server1.id}", "${aws_instance.server2.id}"]
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  security_groups = ["${aws_security_group.ec2-elb-sg.name}"]

  listener {
    instance_port = 80
    instance_protocol = "tcp"
    lb_port = 80
    lb_protocol = "tcp"
  }

  listener {
    instance_port = 443
    instance_protocol = "http"
    lb_port = 443
    lb_protocol = "https"
    ssl_certificate_id = "arn:aws:elasticloadbalancing:us-east-1:079534166449:loadbalancer/app/new-config-elb/442411b66325b7e0"
  }

  health_check {
    target = "HTTP:80/"
    healthy_threshold = 2
    unhealthy_threshold = 2
    interval = 30
    timeout = 5
  }
}

resource "aws_autoscaling_attachment" "asg_attachment_bar" {
  autoscaling_group_name = aws_autoscaling_group.bar.id
  elb                    = aws_elb.default.id
}

data "aws_iam_policy_document" "website_policy" {
  statement {
    actions = [
      "s3:GetObject"
    ]
    principals {
      identifiers = ["*"]
      type = "AWS"
    }
    resources = [
      "arn:aws:cloudfront::079534166449:distribution/E3L5LFQFHPYIDN"
    ]
  }
}

resource "aws_s3_bucket" "b" {
  bucket = "s3-website-test.hashicorp.com"
  acl    = "public-read"
  policy = data.aws_iam_policy_document.website_policy.json

  website {
    index_document = "index.html"
    error_document = "index.html"

    routing_rules = <<EOF
[{
    "Condition": {
        "KeyPrefixEquals": "docs/"
    },
    "Redirect": {
        "ReplaceKeyPrefixWith": "documents/"
    }
}]
EOF
  }
}

locals {
  s3_origin_id = "myS3Origin"
}

resource "aws_cloudfront_distribution" "s3_distribution" {
  origin {
    domain_name = aws_s3_bucket.b.bucket_regional_domain_name
    origin_id   = local.s3_origin_id

    s3_origin_config {
      origin_access_identity = "origin-access-identity/cloudfront/ABCDEFG1234567"
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Some comment"
  default_root_object = "index.html"

  logging_config {
    include_cookies = false
    bucket          = "mylogs.s3.amazonaws.com"
    prefix          = "myprefix"
  }

  aliases = ["thechatproject.tk"]

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = local.s3_origin_id

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "allow-all"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  # Cache behavior with precedence 0
  ordered_cache_behavior {
    path_pattern     = "/content/immutable/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = local.s3_origin_id

    forwarded_values {
      query_string = false
      headers      = ["Origin"]

      cookies {
        forward = "none"
      }
    }

    min_ttl                = 0
    default_ttl            = 86400
    max_ttl                = 31536000
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
  }

  # Cache behavior with precedence 1
  ordered_cache_behavior {
    path_pattern     = "/content/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = local.s3_origin_id

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
  }

  price_class = "PriceClass_200"

  restrictions {
    geo_restriction {
      restriction_type = "whitelist"
      locations        = ["US"]
    }
  }

  tags = {
    Environment = "production"
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

