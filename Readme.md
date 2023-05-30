# API de Consulta de Unidad de Fomento (UF)

Esta API permite consultar el valor de la Unidad de Fomento (UF) para una fecha específica utilizando scraping en el sitio web del Servicio de Impuestos Internos (SII) de Chile.
Tiene rangos de fecha valido empezando con fechas superiores a 01-01-2013 y no siendo superior 11 días a la fecha actual, ni años superiores al año actual.

## Indice

1. [ Instalación ](#instalación)
2. [ endpoints disponibles ](#endpoints-disponibles)

## Instalación

1. Clona el repositorio:

```bash
git clone git@github.com:JoseJulianMosqueraFuli/fapro-test.git
```

2. Navegar al directorio clonado:

```bash
cd fapro-test
```

3. Cree y ejecute el contenedor Docker:

```bash
docker-compose up --build
```

4. La API ahora debería estar disponible en http://localhost:8000/

5. Si requiere ejecutar prueba:

```bash
docker-compose run fastapi python3 -m pytest
```

## Endpoints disponibles

### UF

#### POST /uf

```jsx
http://localhost:8000/uf
```

Entrada

```jsx
{
    "date" : "01-01-2023"
}
```

Respuesta

```jsx
{
    "uf_value": "35.122,26"
}
```

#### Mejoras :

- Agregar una base de datos de caché para crear un sistema de confiabilidad.
- Agregar nuevas características.

### Autor

Creado por Jose Julian Mosquera Fuli.
