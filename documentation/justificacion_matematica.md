# SHA-1 NL v1.0 — Justificación matemática

## 1. Objetivo

SHA-1 NL es una variante experimental y educativa basada en la estructura de SHA-1. Conserva el padding, bloques de 512 bits, palabras de 32 bits, 80 iteraciones, cinco registros de estado y salida de 160 bits. Modifica la expansión de palabras y las funciones booleanas utilizadas en los cuatro grupos de iteraciones.

No se afirma que la variante sea criptográficamente segura ni más resistente que SHA-1.

## 2. Aritmética de 32 bits

Todas las palabras pertenecen a `Z/(2^32)`. La suma se calcula módulo `2^32`. Las operaciones AND, XOR y NOT se aplican bit a bit. NOT se enmascara con `0xFFFFFFFF`. La rotación circular conserva exactamente 32 bits.

## 3. Expansión personalizada

Para las primeras 16 palabras se conserva la lectura big-endian del bloque de 512 bits. Para `16 <= t <= 79` se define:

`Q(x,y,z) = (x AND y) XOR (x AND z) XOR (y AND z)`

`W[t] = ROTL1(Q(W[t-3], W[t-8], W[t-14]) XOR W[t-16])`

Q es la función mayoría de tres entradas. Su forma algebraica sobre GF(2) es `xy XOR xz XOR yz`, de grado algebraico 2, por lo que no es afín. Su tabla de verdad produce cuatro ceros y cuatro unos.

## 4. Funciones de compresión personalizadas

Se define la función de selección:

`S(x,y,z) = (x AND y) XOR ((NOT x) AND z)`

En forma algebraica sobre GF(2), bit a bit:

`S(x,y,z) = xy XOR z XOR xz`

Aparecen términos producto, por lo que su grado algebraico es 2 y no es afín. Para cada asignación de x, la salida selecciona y cuando x=1 y z cuando x=0. La función es equilibrada: para las ocho entradas posibles hay cuatro salidas 0 y cuatro salidas 1.

Las funciones por bloque son:

- Iteraciones 0–19: `F1(B,C,D) = S(C,B,D)`.
- Iteraciones 20–39: `F2(B,C,D) = S(D,C,B)`.
- Iteraciones 40–59: `F3(B,C,D) = S(B,D,C)`.
- Iteraciones 60–79: `F4(B,C,D) = S(C,D,B)`.

Las permutaciones cambian qué registro actúa como selector y cuáles son las entradas seleccionadas.

## 5. Ecuación de ronda

La actualización conserva la estructura de SHA-1:

`TEMP = (ROTL5(A) + F_i(B,C,D) + E + W[t] + K_i) mod 2^32`

Después:

`A'=TEMP; B'=A; C'=ROTL30(B); D'=C; E'=D`.

Se mantienen las cuatro constantes de ronda originales de SHA-1.

## 6. Padding y salida

Se conserva el padding estándar: se agrega un bit 1, después ceros hasta que queden 64 bits disponibles al final del bloque, y finalmente la longitud original del mensaje en 64 bits big-endian. El resultado concatena cinco palabras de 32 bits y se representa como 40 dígitos hexadecimales.

## 7. Alcance y limitaciones

El grado algebraico 2 y el balance de las funciones son propiedades locales de las funciones booleanas; no prueban resistencia a colisiones, preimagen, segunda preimagen ni ataques diferenciales. Cambiar funciones dentro de una construcción hash no garantiza mayor seguridad. SHA-1 NL se presenta exclusivamente como ejercicio académico y no debe emplearse para contraseñas, firmas digitales ni datos sensibles.
