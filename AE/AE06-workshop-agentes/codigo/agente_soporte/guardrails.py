"""Ejercicio 7. Guardarraíles: datos sensibles, acciones peligrosas, límite de pasos y validación de la salida."""
import re
from pydantic import BaseModel, Field, field_validator

DNI = re.compile(r"\b[XYZ]?\d{7,8}[A-Z]\b", re.I)
TARJETA = re.compile(r"\b(?:\d[ -]?){13,19}\b")
IBAN = re.compile(r"\bES\d{2}(?:[ ]?\d{4}){5}\b", re.I)
PELIGROSO = re.compile(r"\b(borra|elimina|vacía|vacia|drop|truncate)\b.*\b(pedidos|clientes|base de datos|tabla|todo)\b", re.I)

def _luhn(num: str) -> bool:
    d = [int(c) for c in re.sub(r"\D", "", num)][::-1]
    return len(d) >= 13 and sum(d[0::2] + [sum(divmod(2 * x, 10)) for x in d[1::2]]) % 10 == 0

def revisar_entrada(texto: str) -> tuple[str, list[str]]:
    """Enmascara datos sensibles antes de enviarlos al LLM y devuelve avisos."""
    avisos = []
    if DNI.search(texto): texto = DNI.sub("[DNI OCULTO]", texto); avisos.append("DNI/NIE detectado y ocultado: no es necesario para gestionar pedidos.")
    for m in TARJETA.findall(texto):
        if _luhn(m): texto = texto.replace(m, "[TARJETA OCULTA]"); avisos.append("Número de tarjeta detectado y ocultado: nunca lo compartas por chat.")
    if IBAN.search(texto): texto = IBAN.sub("[IBAN OCULTO]", texto); avisos.append("IBAN detectado y ocultado.")
    return texto, avisos

def es_peligrosa(texto: str) -> bool:
    return bool(PELIGROSO.search(texto))

class RespuestaFinal(BaseModel):
    """Esquema que debe cumplir la respuesta final antes de mostrarse."""
    texto: str = Field(min_length=2, max_length=1500)
    @field_validator("texto")
    @classmethod
    def sin_fugas(cls, v):
        bajo = v.lower()
        if "<tool_call>" in bajo or '"name":' in bajo: raise ValueError("la respuesta contiene una llamada a herramienta sin ejecutar")
        if "eres el asistente" in bajo: raise ValueError("la respuesta filtra el prompt de sistema")
        if re.search(r"\[(consultar_pedido|calcular_presupuesto|crear_incidencia|buscar_producto|validar_email|recordar_dato)", v):
            raise ValueError("la respuesta menciona herramientas en lugar de ejecutarlas")
        return v.strip()
