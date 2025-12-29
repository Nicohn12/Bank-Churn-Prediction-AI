
CREATE TABLE clientes_raw (
    "RowNumber" int,
    "CustomerId" int,
    "Surname" varchar,
    "CreditScore" int,
    "Geography" varchar,
    "Gender" varchar,
    "Age" int,
    "Tenure" int,
    "Balance" numeric,
    "NumOfProducts" int,
    "HasCrCard" int,
    "IsActiveMember" int,
    "EstimatedSalary" numeric,
    "Exited" int
);

)
CREATE VIEW vista_para_ml AS
SELECT 
    "CustomerId",
    "CreditScore",
    "Geography",
    CASE WHEN "Gender" = 'Female' THEN 1 ELSE 0 END AS es_mujer,
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
    "Exited"
FROM clientes_raw;

CREATE VIEW informe_powerbi AS
SELECT 
    c."CustomerId",
    c."Surname" as apellido,
    c."Geography" as pais,
    c."CreditScore",
    c."Gender" as genero,
    c."Age" as edad,
    c."Tenure",
    c."Balance", 
    c."NumOfProducts",
    c."HasCrCard",
    c."IsActiveMember",
    c."EstimatedSalary",
    c."Exited",
    r."Probabilidad_Fuga",
    CASE
        WHEN r."Probabilidad_Fuga" > 0.8 THEN 'Riesgo ALTO '
        WHEN r."Probabilidad_Fuga" > 0.5 THEN 'Riesgo MEDIO '
        ELSE 'Riesgo BAJO '
    END AS "Riesgo calculado",
    (c."Balance" * r."Probabilidad_Fuga") AS perdida_esperada
FROM clientes_raw c
LEFT JOIN resultados_prediccion r ON r."CustomerId" = c."CustomerId";