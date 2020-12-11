Description
-----------

[![Build Status](https://travis-ci.org/mergermarket/terraform-acuris-backend-lambda-routing.svg?branch=master)](https://travis-ci.org/mergermarket/terraform-acuris-backend-lambda-routing)

This module creates the DNS and routing rule for a backend lambda. It's an
opinionated module that forms the DNS name from the `env` (environment name),
`name` (short name for the service - typically with the "-service" suffix
removed) and `domain`.

For the live environment this will be:

    name.domain

For the non-live environments this will be:

    env-name.domain

This is intended for use in a backend router component (i.e. one created from
https://github.com/mergermarket/backend-router-boilerplate).

Usage
-----

Add this to the bottom of the `infra/main.tf` file in your backend router for
each service:
```
    module "cognito_service" {
      source  = "mergermarket/backend-service-routing/acuris"
      version = "0.0.2"
    
      env              = "${var.env}"
      component_name   = "cognito-service"
      dns_domain       = "${var.dns_domain}"
      priority         = "10"
      alb_listener_arn = "${module.backend_router.alb_listener_arn}"
      alb_dns_name     = "${module.backend_router.alb_dns_name}"
      vpc_id           = "${var.platform_config["vpc"]}"
      aws_account_alias = "alias"
      backend_dns       = "backend.com"
      lambda_arn        = "${var.lambda_arn}"
    }
```
