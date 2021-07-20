#!/bin/sh

echo "Getting data..."
curl -sS https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19VacunasAgrupadas.csv.zip > Covid19VacunasAgrupadas.csv.zip && \
unzip Covid19VacunasAgrupadas.csv.zip                                  && \
rm Covid19VacunasAgrupadas.csv.zip

export PGPASSWORD=$2

echo "Dropping existing tables..."
psql -U $1 -d $3 -h $4 -c "DROP TABLE IF EXISTS datos"

echo "Creating new table..."
psql -U $1 -d $3 -h $4 -c "CREATE TABLE datos
(
    jurisdiccion_codigo_indec integer, 
    jurisdiccion_nombre text,
    vacuna_nombre text,
    primera_dosis_cantidad integer,
    segunda_dosis_cantidad integer
);"

echo "Populating table..."
psql -U $1 -d $3 -h $4 -c "\copy datos FROM 'Covid19VacunasAgrupadas.csv' DELIMITER ',' CSV HEADER;"

echo "Adding id parameter..."
psql -U $1 -d $3 -h $4 -c "ALTER TABLE datos ADD COLUMN id SERIAL PRIMARY KEY;"

echo "Deleting data file..."
rm Covid19VacunasAgrupadas.csv