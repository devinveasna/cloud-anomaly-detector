provider "aws" {
    region = "us-east-1"
}

resource "aws_security_group" "instance_sg" {
    name = "instance-security-group"
    description = "Allow SSH inbound traffic"

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_iam_role" "ec2_cloudwatch_role" {
    name = "ec2_cloudwatch_read_only_role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17",
        Statement = [{
            Action = "sts:AssumeRole",
            Effect = "Allow",
            Principal = { Service = "ec2.amazonaws.com" },
        }],
    })
}

resource "aws_iam_role_policy_attachment" "cloudwatch_read_only_attachment" {
  role = aws_iam_role.ec2_cloudwatch_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchReadOnlyAccess"
}

resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "ec2_instance_profile"
  role = aws_iam_role.ec2_cloudwatch_role.name
}


resource "aws_instance" "monitored_server" {
  ami = "ami-08a6efd148b1f7504"
  
  instance_type = "t2.micro"
  
  security_groups = [aws_security_group.instance_sg.name]
  iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name

  tags = {
    Name    = "Monitored-Server-Project"
    Project = "Cloud-Anomaly-Detector"
  }
}

output "instance_id" {
  description = "The ID of the EC2 instance created"
  value = aws_instance.monitored_server.id
}

output "public_ip" {
  description = "Public IP address of the EC2 instance"
  value = aws_instance.monitored_server.public_ip
}