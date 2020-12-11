locals {
  logical_dns_service_name = "${var.override_dns_name != "" ? var.override_dns_name : replace(var.component_name, "/-service$/", "")}"
  env_prefix               = "${var.env == "live" ? "" : "${var.env}-"}"
  target_host_name         = "${local.env_prefix}${local.logical_dns_service_name}.${var.dns_domain}"
}

resource "aws_alb_listener_rule" "rule" {
  listener_arn = "${var.alb_listener_arn}"
  priority     = "${var.priority}"

  action {
    type             = "forward"
    target_group_arn = "${aws_alb_target_group.target_group.arn}"
  }

  condition {
    field  = "host-header"
    values = ["${local.target_host_name}"]
  }

  condition {
    field  = "path-pattern"
    values = ["*"]
  }
}

locals {
  old_target_group_name = "${replace(replace("${var.env}-${var.component_name}", "/(.{0,32}).*/", "$1"), "/^-+|-+$/", "")}"

  target_group_name_hash    = "${base64encode(base64sha256("${var.env}-${var.component_name}"))}"
  target_group_name_postfix = "${replace(replace("${local.target_group_name_hash}", "/(.{0,12}).*/", "$1"), "/^-+|-+$/", "")}"
  target_group_name_prefix  = "${replace(replace("${var.env}-${var.component_name}", "/(.{0,20}).*/", "$1"), "/^-+|-+$/", "")}"
  target_group_name         = "${local.target_group_name_prefix}${local.target_group_name_postfix}"
}

resource "aws_alb_target_group" "target_group" {
  name = "${var.hash_target_group_name ? local.target_group_name : local.old_target_group_name}"
  target_type = "lambda"

  lifecycle {
    create_before_destroy = true
  }

  tags {
    component = "${var.component_name}"
    env       = "${var.env}"
    service   = "${var.env}-${var.component_name}"
  }
}

resource "aws_lb_target_group_attachment" "target_group_attachment" {
  target_group_arn = "${aws_alb_target_group.target_group.arn}"
  target_id        = "${var.lambda_arn}"
}

resource "aws_lambda_permission" "with_lb" {
  statement_id  = "AllowExecutionFromlb"
  action        = "lambda:InvokeFunction"
  function_name = "${var.lambda_arn}"
  principal     = "elasticloadbalancing.amazonaws.com"
  source_arn    = "${aws_alb_target_group.target_group.arn}"
}

locals {
  logical_service_name = "${var.env}-${replace(var.component_name, "/-service$/", "")}"
  full_account_name    = "${var.env == "live" ? "${var.aws_account_alias}prod" : "${var.aws_account_alias}dev"}"
  backend_dns_domain   = "${local.full_account_name}.${var.backend_dns}"
  backend_dns_record   = "${local.logical_service_name}.${local.backend_dns_domain}"
}

data "aws_route53_zone" "dns_domain" {
  name = "${local.backend_dns_domain}"
}

resource "aws_route53_record" "dns_record" {
  zone_id = "${data.aws_route53_zone.dns_domain.zone_id}"
  name    = "${local.backend_dns_record}"

  type            = "CNAME"
  records         = ["${var.alb_dns_name}"]
  ttl             = "${var.ttl}"
  allow_overwrite = "${var.allow_overwrite}"

  depends_on = ["aws_alb_listener_rule.rule"]
}
