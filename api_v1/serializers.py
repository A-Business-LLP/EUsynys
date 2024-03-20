from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import serializers
from .models import Table, Region


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')


class RegionTablesSerializer(serializers.ModelSerializer):
    total_tables = serializers.SerializerMethodField()
    total_responses = serializers.SerializerMethodField()
    details_by_order_sent = serializers.SerializerMethodField()
    details_by_results = serializers.SerializerMethodField()
    total_submissions_not_reviewed = serializers.SerializerMethodField()  # Добавлено новое поле
    details_by_order_sent_responses = serializers.SerializerMethodField()
    details_by_results_responses = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = (
            'id',
            'name', 
            'total_tables', 
            'total_responses', 
            'details_by_order_sent', 
            'details_by_results',
            'total_submissions_not_reviewed',
            'details_by_order_sent_responses',  # Добавляем новые поля в вывод
            'details_by_results_responses',
        )

    def get_total_tables(self, obj):
        return obj.tables.count()

    def get_total_responses(self, obj):
        return obj.tables.exclude(response_received__isnull=True).count()

    def get_details_by_order_sent(self, obj):
        details = {}
        for choice in Table.TableWhereOrderSent.choices:
            details[str(choice[1])] = obj.tables.filter(where_order_sent=choice[0]).count()
        return details

    def get_details_by_results(self, obj):
        details = {}
        for choice in Table.TableResults.choices:
            details[str(choice[1])] = obj.tables.filter(results=choice[0]).count()
        return details

    def get_total_submissions_not_reviewed(self, obj):
        # Вычисляем количество объектов Table с submissions_reviewed_deadline=False
        return obj.tables.filter(submissions_reviewed_deadline=False).count()

    def get_details_by_order_sent_responses(self, obj):
        details = {}
        for choice in Table.TableWhereOrderSent.choices:
            # Считаем количество записей с данным choice, где есть ответ
            count = obj.tables.filter(where_order_sent=choice[0], response_received__isnull=False).count()
            details[str(choice[1])] = count
        return details

    def get_details_by_results_responses(self, obj):
        details = {}
        for choice in Table.TableResults.choices:
            # Считаем количество записей с данным choice, где есть ответ
            count = obj.tables.filter(results=choice[0], response_received__isnull=False).count()
            details[str(choice[1])] = count
        return details


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'region', 'number', 'calendar', 'article_сriminal_сode', 'performance', 'date_referral', 'where_order_sent', 'review_period', 'response_received', 'results', 'submissions_reviewed_deadline']
        extra_kwargs = {'submissions_reviewed_deadline': {'read_only': True}}
