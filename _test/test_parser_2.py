# https://github.com/macbre/sql-metadata/blob/master/README.md

from sql_metadata import Parser

sql = """


with product_actual_n_row as (
    select old_product_id, new_product_id, row_number() over (partition by old_product_id order by new_product_id desc) n_row
    from sch_NORMALIZED_MASTERDATA_IT.D_PRODUCT_ACTUAL
),

no_dupl_product_actual as (
    select old_product_id, new_product_id
    from product_actual_n_row
    where n_row = 1
),

sales_kpis as (
    select
        2 as model_id,
        'LY' as scenario_id,
        a.year_month_sales_dt as year_month_id,
        a.sold_to_customer_id as customer_id,
        coalesce(d.MODEL_PRODUCT_ID, c.new_product_id, a.product_id) as product_id,
        a.sales_organization_id,
        sum(a.net_invoice_hl_vl) as net_invoice_hl_vl,
        sum(a.promotional_hl_vl) as promotional_hl_vl
    from sch_DATAMART_SALES_IT.F_SALES_TMP1 a

    left join sch_NORMALIZED_MASTERDATA_IT.D_NOT_CONFORMED_PALLETTIZATION_PRODUCT d
        on a.product_id = d.PRODUCT_ID

    left join no_dupl_product_actual c
        on a.product_id = c.old_product_id

    where 1=1
        and year(a.sales_dt) >= 2023 --we keep qlik volumes until 2022
        and a.year_month_sales_dt <= (select max(year_month_id) from sch_NORMALIZED_ALA_IT.F_ALA_COPA_CFIN_ACT) --take volumes until last year-month from cfin
    group by 1,2,3,4,5,6
),

cfin_sales as (
    select 
        nvl(a.model_id,b.model_id) as model_id,
        nvl(a.scenario_id,b.scenario_id) as scenario_id,
        nvl(a.year_month_id,b.year_month_id) as year_month_id,
        nvl(a.customer_id,b.customer_id) as customer_id,
        nvl(a.product_id,b.product_id) as product_id,
        nvl(a.sales_organization_id,b.sales_organization_id) as sales_organization_id,

        a.`GROSS_REVENUE_WITHOUT_EXCISE_DUTY_VL`,
  a.`SCP_CIFRA_FISSA_VL`,
  a.`YEB_LIV_2_PERC_VL`,
  a.`COSTI_FISSI_PRODUZIONE_ACT_VL`,
  a.`ALTRI_COSTI_LOGISTICA_ACT_VL`,
  a.`LAVORAZIONI_ESTERNE_ACT_BASE_VL`,
  a.`OTHER_PACKAGING_MATERIALS_CRED_VL`,
  a.`PROCEED_FROM_SERVICES_VL`,
  a.`ADVERTISING_MEDIA_EXPENSES_VL`,
  a.`RAW_MATERIALS_ACT_BASE_VL`,
  a.`EDLP_DISCOUNT_VL`,
  a.`AUXILIARY_AND_OTHER_MATERIALS_ACT_BASE_VL`,
  a.`SPONSORSHIP_VL`,
  a.`YEB_CIFRA_FISSA_VL`,
  a.`COSTI_FISSI_COMMERCIALI_VL`,
  a.`AUXILIARY_AND_OTHER_MATERIALS_STD_VL`,
  a.`BAD_DEBTS_VL`,
  a.`DCP_SCONTO_CASSA_VL`,
  a.`NAVETTAGGIO_RESTOCKING_VL`,
  a.`PARASSITE_INTERBREWERY_STD_VL`,
  a.`OTHER_RAW_MATERIALS_SCRAP_VL`,
  a.`STOCK_MOVEMENT_VL`,
  a.`PROMOTIONAL_VL`,
  a.`TRASPORT_BULK_STD_VL`,
  a.`YEB_PERC_VL`,
  a.`SCP_LIV_2_PERC_G_VL`,
  a.`NET_GROUP_LICENSE_FEES_VL`,
  a.`OMITTED_DISCOUNT_VL`,
  a.`INSEGNE_VL`,
  a.`LAVORAZIONI_ESTERNE_STD_VL`,
  a.`IMPORTED_PRODUCTS_STD_VL`,
  a.`MERCHANDISING_VL`,
  a.`EXCISE_DUTY_REVENUE_VL`,
  a.`AGENT_FEE_VL`,
  a.`VOLUMI_INTERCOMPANY_VL`,
  a.`OTHER_PACKAGING_MATERIALS_ACC_VL`,
  a.`FACCHINAGGIO_STD_VL`,
  a.`PACKAGING_MATERIALS_STD_VL`,
  a.`ONE_STAC_COSTI_RICAVI_VL`,
  a.`SCONTO_ETTOLITRICO_VL`,
  a.`ACQ_SPAZI_VISIBILITY_VL`,
  a.`LISTING_VL`,
  a.`SCP_PERC_VL`,
  a.`HANDLING_DEPOSIT_STD_VL`,
  a.`RETURN_VL`,
  a.`ACCISA_COGS_DIBEVIT_VL`,
  a.`OTHER_RAW_MATERIALS_ACC_VL`,
  a.`EXPIRING_PRODUC_DISCOUNT_VL`,
  a.`RAW_MATERIALS_STD_VL`,
  a.`ADVERTISING_DEVELOPMENT_VL`,
  a.`PROMO_AL_CONSUMO_VL`,
  a.`OTHER_RAW_MATERIALS_WR_VL`,
  a.`PROMO_AL_TRADE_VL`,
  a.`BIRRA_OMAGGIO_VL`,
  a.`ENERGY_AND_WATER_STD_VL`,
  a.`MARKET_RESEARCH_VL`,
  a.`TRASFERIMENTI_PRODOTTI_FINITI_INTERBREWERY_VL`,
  a.`COSTI_FISSI_SUPPORT_FUNCTION_VL`,
  a.`OFF_INVOICE_DISCOUNT_INTERCOMPANY_VL`,
  a.`SHUTTLING_STD_VL`,
  a.`COSTI_FISSI_LOGISTICA_STD_VL`,
  a.`CO_MARKETING_VL`,
  a.`OTHER_AUXILIARY_MATERIALS_SCRAP_VL`,
  a.`HANDLING_WAREHOUSE_STD_VL`,
  a.`ECOTAX_VL`,
  a.`COSTI_FISSI_PRODUZIONE_STD_VL`,
  a.`VOLUME_NOPROMO_VL_VL`,
  a.`DELIVERY_AL_CLIENTE_STD_VL`,
  a.`OTHER_MKTING_EXPENSES_VL`,
  a.`BASE_PRICE_DISCOUNT_VL`,
  a.`EXCISE_DUTY_COST_VL`,
  a.`PROMO_PRICE_DISCOUNT_VL`,
  a.`TRASPORTI_STAC_VL`,
  a.`OTHER_LOGISTIC_COSTS_STD_VL`,
  a.`COSTI_FISSI_LOGISTICA_ACT_VL`,
  a.`OTHER_PACKAGING_MATERIALS_WR_VL`,
  a.`SELL_OUT_CREDIT_NOTES_VL`,
  a.`PACKAGING_MATERIALS_ACT_BASE_VL`,
  a.`LOGISTIC_DISCOUNT_VL`,
  a.`YEB_POC_VL`,
  a.`ENERGY_AND_WATER_ACT_VL`,
  a.`STRUCTURAL_INTERBREWERY_STD_VL`,
  a.`SPECIAL_PRICE_DISCOUNT_VL`,
  a.`HANDLING_DI_DEPOSITO_HK_VL`,
  a.`CATERING_VL`,
  a.`GASOLIO_VL`,
  a.`EXTRA_COSTI_LOG_SEMILAVORATO_VL`,
  a.`OTHER_PRODOTTI_IMPORTATI_VL`,
  a.`DELIVERY_FEE_VL`,
  a.`OTHER_AUXILIARY_MATERIALS_WR_VL`,
  a.`FACCHINAGGIO_VL`,
  a.`POP_COGS_VL`,
  a.`SMALTIMENTO_PRODOTTI_IMPORTATI_VL`,
  a.`FUEL_STD_VL`,
  a.`BRAND_DEVELOPMENT_VL`,
  a.`DISPUTE_DISCOUNT_VL`,
  a.`CUT_PRICE_INTERCOMPANY_VL`,
  a.`FREE_GOODS_DISCOUNT_VL`,
  a.`VOLUMI_VL_VL`,
  a.`OTHER_PACKAGING_MATERIALS_SCRAP_VL`,
  a.`ADDITIONAL_DISCOUNT_VL`,
  a.`COSTI_FISSI_STAC_VL`,
  a.`INTERNATIONAL_AGREEMENT_VL`,
  a.`HANDLING_DI_STABILIMENTO_VL`,
  a.`DCP_SCONTO_FINANZIARIO_VL`,
  a.`GROSS_REVENUE_VL`,
  a.`PARASSITE_INTERBREWERY_ACT_VL`,
  a.`EX_BTL_VL`,
  a.`RAW_MATERIALS_ACT_VL`,
  a.`PRIMARY_LnD_GENERAL_VARIABLE_EXP_VL`,
  a.`HANDLING_WAREHOUSE_ACT_VL`,
  a.`STRUCTURAL_INTERBREWERY_ACT_VL`,
  a.`TRANSPORT_CUST_RECOVERY_VL`,
  a.`DCP_VL`,
  a.`PRODUCTS_BIFR_VL`,
  a.`PACKAGING_MATERIALS_ACT_VL`,
  a.`PRIMARY_TRANSPORTATION_VARIABLE_EXP_VL`,
  a.`INVENTORY_MOVEMENT_FnV_VL`,
  a.`OTHER_COMMERCIAL_VARIABLE_EXP_VL`,
  a.`TRANSPORT_CUST_PRIMARY_VL`,
  a.`CUT_PRICE_VL`,
  a.`HANDLING_DEPOSIT_ACT_VL`,
  a.`SECONDARY_TRANSPORTATION_VARIABLE_EXP_VL`,
  a.`SHUTTLING_ACT_VL`,
  a.`DELIVERY_AL_CLIENTE_ACT_VL`,
  a.`OTHER_LOGISTIC_COSTS_ACT_VL`,
  a.`IMPORTED_PRODUCTS_ACT_VL`,
  a.`PRIMARY_WAREHOUSING_VARIABLE_EXP_VL`,
  a.`SCP_VL`,
  a.`AUXILIARY_AND_OTHER_MATERIALS_ACT_VL`,
  a.`FACCHINAGGIO_ACT_VL`,
  a.`LAVORAZIONI_ESTERNE_ACT_VL`,
  a.`TRANSPORT_BETWEEN_WAREHOUSE_VL`,
  a.`TOTAL_FIXED_COST_STD_VL`,
  a.`TRASPORT_BULK_ACT_VL`,
  a.`FUEL_ACT_VL`,
  a.`OTHER_VARIABLE_EXPENSES_VL`,
  a.`YEB_VL`,
  a.`PRIMARY_TRANSPORTATION_INTERNAL_OPERATION_VL`,
  a.`BTL_VL`,
  a.`OFF_INVOICE_DISCOUNT_VL`,
  a.`NET_TURNOVER_VL`,
  a.`ATL_VL`,
  a.`COGS_ACT_VL`,
  a.`LOGS_STD_VL`,
  a.`EXCISE_DUTIES_&_CONAI_VL`,
  a.`COGS_STD_VL`,
  a.`OTHER_COGS_VL`,
  a.`REVENUE_VL`,
  a.`TOTAL_VARIABLE_EXPENSES_STD_VL`,
  a.`TOTAL_ABTL_VL`,
  a.`TOTAL_VARIABLE_EXPENSES_ACT_VL`,
  a.`GROSS_PROFIT_NET_STD_VL`,
  a.`GROSS_PROFIT_ACT_VL`,
  a.`GROSS_PROFIT_NET_ACT_VL`,
  a.`TOTAL_FIXED_COST_ACT_VL`,
  a.`GROSS_PROFIT_STD_VL`,
  a.`LOGS_ACT_VL`,

        case when nvl(a.year_month_id,b.year_month_id) >= '202301' then b.net_invoice_hl_vl else a.VOLUME_VL end as VOLUME_VL,
        case when nvl(a.year_month_id,b.year_month_id) >= '202301' then b.promotional_hl_vl else a.VOLUME_PROMO_VL_VL end as VOLUME_PROMO_VL_VL


    from sch_NORMALIZED_ALA_IT.F_ALA_COPA_CFIN_ACT a

    full outer join sales_kpis b
        on a.model_id = b.model_id
        and a.year_month_id = b.year_month_id
        and a.scenario_id = b.scenario_id
        and a.customer_id = b.customer_id
        and a.product_id = b.product_id
        and a.sales_organization_id = b.sales_organization_id
)

select 
    

    xxhash64(model_id,year_month_id,scenario_id,customer_id,product_id,sales_organization_id)

 as ALA_COPA_CFIN_ACT_PK,
    

    xxhash64(customer_id,sales_organization_id)

 as COMMERCIAL_HIERARCHY_LOCAL_ALA_FK,
    

    xxhash64(customer_id,sales_organization_id)

 as CUSTOMER_HIERARCHY_ALA_FK,
    *,

    
	
    '0' as load_id,
    from_utc_timestamp(current_timestamp(),'Europe/Rome')::timestamp as dwh_update_dt



from cfin_sales

where 1=1
"""
# for tk in Parser(sql).tokens:
    # print(tk.value)

# startswith with (non per select)
pql = Parser(sql)
print(f"===== generalize")
print(pql.generalize)
print(f"===== columns")
print(pql.columns)

'''
for wt in pql.with_queries.keys():
    print("======", wt)
    print(pql.with_queries[wt])
'''

# startswith select 
pql_with = Parser(pql.with_queries['cfin_sales'])
print(f"===== generalize")
print(pql_with.generalize)
print(f"===== columns")
print(pql_with.columns)
print(f"===== columns_aliases") # ERRATO: {'n_row': ['old_product_id', 'new_product_id']}
print(pql_with.columns_aliases)
print(f"===== columns_aliases_dict")
print(pql_with.columns_aliases_dict)
print(f"===== columns_dict")
print(pql_with.columns_dict)
print(f"===== query")
print(pql_with.query)
print(f"===== tables")
print(pql_with.tables)

single_row_list = list()
single_row = ''
brackets_count = 0
columns_list = list()
for tk in pql_with.tokens:
    print(tk.value)
    if tk.value == 'select':
        continue
    elif brackets_count == 0 and tk.value == 'from':
        columns_list.append(single_row_list)
        break
    elif tk.value in ('(', '['):
        single_row_list.append(tk.value)
        single_row += tk.value
        brackets_count += 1
        print('--> brackets_count++')
    elif tk.value in (')', ']'):
        single_row_list.append(tk.value)
        brackets_count -= 1
        print('--> brackets_count--')
    elif brackets_count == 0 and tk.value in (','):
        columns_list.append(single_row_list)
        single_row_list = list()
    else:
        single_row_list.append(tk.value)

for col in columns_list:
    print("col name:", col[-1])
    print("col formula:", col[:-1])

# SQLToken(position=1030,value=customer_id,is_keyword=False,is_name=True,is_punctuation=False,is_dot=False,is_wildcard=False,is_integer=False,is_float=False,is_comment=False,is_as_keyword=False,is_left_parenthesis=False,is_right_parenthesis=False,last_keyword=SELECT,next_token=,,previous_token=(,subquery_level=0,token_type=None,is_in_nested_function=True,parenthesis_level=1,is_subquery_start=False,is_subquery_end=False,is_with_query_start=False,is_with_query_end=False,is_with_columns_start=False,is_with_columns_end=False,is_nested_function_start=False,is_nested_function_end=False,is_column_definition_start=False,is_column_definition_end=False,is_create_table_columns_declaration_start=False,is_create_table_columns_declaration_end=False,is_partition_clause_start=False,is_partition_clause_end=False)

