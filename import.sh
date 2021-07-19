#!/bin/sh

echo "Getting data"
curl -sS https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19VacunasAgrupadas.csv.zip > Covid19VacunasAgrupadas.csv.zip && \
unzip Covid19VacunasAgrupadas.csv.zip                                  && \
rm Covid19VacunasAgrupadas.csv.zip

export PGPASSWORD=$4

echo "Creating table"
psql -h $1 -d $2 -U $3 -c "DROP table if exists datos"
psql -h $1 -d $2 -U $3 -c "CREATE TABLE datos
(
    jurisdiccion_codigo_indec integer, 
    jurisdiccion_nombre text,
    vacuna_nombre text,
    primera_dosis_cantidad integer,
    segundad_dosis_cantidad integer
);"

echo "Filling table with data"
psql -h $1 -d $2 -U $3 -c "\copy datos from 'Covid19VacunasAgrupadas.csv' DELIMITER ',' CSV HEADER;"

echo "Altering table"
psql -h $1 -d $2 -U $3 -c "ALTER TABLE datos ADD COLUMN id SERIAL PRIMARY KEY;"

echo "Deleting downloaded dataset file"
rm Covid19VacunasAgrupadas.csv