# Generated by Django 4.1.3 on 2022-12-08 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0010_order_razorpay_order_id_order_razorpay_payment_id_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="razorpay_order_id",
            new_name="razor_pay_order_id",
        ),
        migrations.RenameField(
            model_name="order",
            old_name="razorpay_payment_id",
            new_name="razor_pay_payment_id",
        ),
        migrations.RenameField(
            model_name="order",
            old_name="razorpay_signature",
            new_name="razor_pay_payment_signature",
        ),
    ]