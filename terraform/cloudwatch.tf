resource "aws_cloudwatch_log_group" "tomato_webapp" {
  name              = "tomato-webapp"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_group" "tomato_root_server_import" {
  name              = "tomato-root-server-import"
  retention_in_days = 7
}

### Running the root server import
resource "aws_cloudwatch_event_rule" "root_server_import" {
  name                = "tomato-root-server-import"
  description         = "Kicks off root server import every 4 hours"
  schedule_expression = "rate(4 hours)"
}

data "aws_iam_policy_document" "ecs_events" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "ecs_events_run_task_with_any_role" {
  statement {
    effect    = "Allow"
    actions   = ["iam:PassRole"]
    resources = ["*"]
  }

  statement {
    effect    = "Allow"
    actions   = ["ecs:RunTask"]
    resources = [aws_ecs_task_definition.tomato_root_server_import.arn]
  }
}

resource "aws_iam_role" "ecs_events" {
  name               = "ecs-events"
  assume_role_policy = data.aws_iam_policy_document.ecs_events.json
}

resource "aws_iam_role_policy" "ecs_events_run_task_with_any_role" {
  name   = "ecs-events-run-task-with-any-role"
  role   = aws_iam_role.ecs_events.id
  policy = data.aws_iam_policy_document.ecs_events_run_task_with_any_role.json
}

resource "aws_cloudwatch_event_target" "root_server_import" {
  target_id = "tomato-root-server-import"
  arn       = aws_ecs_cluster.main.arn
  rule      = aws_cloudwatch_event_rule.root_server_import.name
  role_arn  = aws_iam_role.ecs_events.arn

  ecs_target {
    launch_type         = "FARGATE"
    task_count          = 1
    task_definition_arn = aws_ecs_task_definition.tomato_root_server_import.arn

    network_configuration {
      security_groups  = [aws_security_group.cluster.id]
      subnets          = [aws_subnet.public_a.id, aws_subnet.public_b.id]
      assign_public_ip = false
    }
  }
}
