// Experimento GVDM14 – mide I1, Q1, Q2, U1, U2 para varios tamaños de colección
const bench = db.getSiblingDB('bench');
bench.phones.drop();
function populatePhones(area, start, stop) {
  for (var i = start; i < stop; i++) {
    var country = 1 + ((Math.random() * 8) << 0);
    var num = (country * 1e10) + (area * 1e7) + i;
    bench.phones.insertOne({ _id: num,
      components: { country: country, area: area, prefix: (i * 1e-4) << 0, number: i },
      display: "+" + country + " " + area + "-" + i });
  }
}
function t(f) { const a = Date.now(); const r = f(); return [Date.now() - a, r]; }
const pasos = [25000, 50000, 100000, 200000, 400000];
let actual = 0; const base = 5550000; const res = [];
for (const total of pasos) {
  const [ti] = t(() => populatePhones(800, base + actual, base + total));
  const insertados = total - actual; actual = total;
  // documento objetivo: el último insertado (se busca por display, NO indexado)
  const obj = bench.phones.find().sort({ $natural: -1 }).limit(1).next();
  const [tq1, n1] = t(() => bench.phones.find({ display: obj.display }).toArray().length);
  const eq1 = bench.phones.find({ display: obj.display }).explain('executionStats').executionStats;
  const [tq2, n2] = t(() => bench.phones.find({ _id: obj._id }).toArray().length);
  const eq2 = bench.phones.find({ _id: obj._id }).explain('executionStats').executionStats;
  const [tu1, r1] = t(() => bench.phones.updateOne({ _id: obj._id }, { $set: { revisado: true } }));
  const [tu2, r2] = t(() => bench.phones.updateMany({ 'components.country': 3 }, { $inc: { 'components.prefix': 1 } }));
  const fila = { docs: total, insertados: insertados, I1_ms: ti, Q1_ms: tq1, Q1_docsExam: eq1.totalDocsExamined, Q1_explain_ms: eq1.executionTimeMillis,
    Q2_ms: tq2, Q2_keysExam: eq2.totalKeysExamined, Q2_explain_ms: eq2.executionTimeMillis,
    U1_ms: tu1, U1_mod: r1.modifiedCount, U2_ms: tu2, U2_mod: r2.modifiedCount };
  res.push(fila); print(JSON.stringify(fila));
}
print('MOTOR=' + db.serverStatus().storageEngine.name);
