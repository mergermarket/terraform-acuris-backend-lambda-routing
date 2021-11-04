import unittest
from subprocess import check_call, check_output


class TestTFBackendRouter(unittest.TestCase):

    def setUp(self):
        check_call(['terraform', 'init', 'test/infra'])

    def test_create_alb_listener_rule_number_of_resources_to_add(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'aws_region=eu-west-1',
            '-var', 'aws_account_alias=awsaccount',
            '-var', 'backend_dns=testbackend.com',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_service_routing.aws_alb_listener_rule.rule',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
Plan: 2 to add, 0 to change, 0 to destroy.
        """.strip() in output

    def test_create_alb_listener_rule(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'aws_region=eu-west-1',
            '-var', 'aws_account_alias=awsaccount',
            '-var', 'backend_dns=testbackend.com',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_service_routing.aws_alb_listener_rule.rule',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_service_routing.aws_alb_listener_rule.rule
      id:                                         <computed>
      action.#:                                   "1"
      action.0.order:                             <computed>
      action.0.target_group_arn:                  "${aws_alb_target_group.target_group.arn}"
      action.0.type:                              "forward"
      arn:                                        <computed>
      condition.#:                                "2"
      condition.1322904213.field:                 "path-pattern"
      condition.1322904213.host_header.#:         <computed>
      condition.1322904213.http_header.#:         "0"
      condition.1322904213.http_request_method.#: "0"
      condition.1322904213.path_pattern.#:        <computed>
      condition.1322904213.query_string.#:        "0"
      condition.1322904213.source_ip.#:           "0"
      condition.1322904213.values.#:              "1"
      condition.1322904213.values.0:              "*"
      condition.3843014500.field:                 "host-header"
      condition.3843014500.host_header.#:         <computed>
      condition.3843014500.http_header.#:         "0"
      condition.3843014500.http_request_method.#: "0"
      condition.3843014500.path_pattern.#:        <computed>
      condition.3843014500.query_string.#:        "0"
      condition.3843014500.source_ip.#:           "0"
      condition.3843014500.values.#:              "1"
      condition.3843014500.values.0:              "dev-cognito.domain.com"
      listener_arn:                               "alb:listener"
      priority:                                   "10"
        """.strip() in output

    def test_create_alb_listener_rule_live(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=live',
            '-var', 'aws_region=eu-west-1',
            '-var', 'aws_account_alias=awsaccount',
            '-var', 'backend_dns=testbackend.com',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_service_routing.aws_alb_listener_rule.rule',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_service_routing.aws_alb_listener_rule.rule
      id:                                         <computed>
      action.#:                                   "1"
      action.0.order:                             <computed>
      action.0.target_group_arn:                  "${aws_alb_target_group.target_group.arn}"
      action.0.type:                              "forward"
      arn:                                        <computed>
      condition.#:                                "2"
      condition.1322904213.field:                 "path-pattern"
      condition.1322904213.host_header.#:         <computed>
      condition.1322904213.http_header.#:         "0"
      condition.1322904213.http_request_method.#: "0"
      condition.1322904213.path_pattern.#:        <computed>
      condition.1322904213.query_string.#:        "0"
      condition.1322904213.source_ip.#:           "0"
      condition.1322904213.values.#:              "1"
      condition.1322904213.values.0:              "*"
      condition.4207679377.field:                 "host-header"
      condition.4207679377.host_header.#:         <computed>
      condition.4207679377.http_header.#:         "0"
      condition.4207679377.http_request_method.#: "0"
      condition.4207679377.path_pattern.#:        <computed>
      condition.4207679377.query_string.#:        "0"
      condition.4207679377.source_ip.#:           "0"
      condition.4207679377.values.#:              "1"
      condition.4207679377.values.0:              "cognito.domain.com"
      listener_arn:                               "alb:listener"
      priority:                                   "10"
        """.strip() in output

    def test_create_aws_alb_target_group(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'aws_region=eu-west-1',
            '-var', 'aws_account_alias=awsaccount',
            '-var', 'backend_dns=testbackend.com',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_service_routing.aws_alb_listener_rule.rule',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
  + module.backend_service_routing.aws_alb_target_group.target_group
      id:                                         <computed>
      arn:                                        <computed>
      arn_suffix:                                 <computed>
      deregistration_delay:                       "300"
      health_check.#:                             <computed>
      lambda_multi_value_headers_enabled:         "false"
      load_balancing_algorithm_type:              <computed>
      name:                                       "dev-cognito-service"
      proxy_protocol_v2:                          "false"
      slow_start:                                 "0"
      stickiness.#:                               <computed>
      tags.%:                                     "3"
      tags.component:                             "cognito-service"
      tags.env:                                   "dev"
      tags.service:                               "dev-cognito-service"
      target_type:                                "lambda"
        """.strip() in output

