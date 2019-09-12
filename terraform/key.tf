data "template_file" "pubkey" {
  template = file(pathexpand("${path.module}/id_rsa.pub"))
}

resource "aws_key_pair" "main" {
  key_name   = "tomato"
  public_key = data.template_file.pubkey.rendered
}

