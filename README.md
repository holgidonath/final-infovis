# final-infovis
COPY datos(jurisdiccion_codigo_indec, jurisdiccion_nombre, vacuna_nombre, primera_dosis_cantidad, segunda_dosis_cantidad)
FROM '\Users\holgerdonath\Deskop\datos.csv'
DELIMITER ','
CSV HEADER;