// Experimento complementario GVDM14: escrituras con confirmación en disco (j:true) e inserción masiva
const b = db.getSiblingDB('bench2'); b.t.drop();
function t(f) { const a = Date.now(); f(); return Date.now() - a; }
const N = 5000;
const motor = db.serverStatus().storageEngine.name;
const tw = t(() => { for (let i = 0; i < N; i++) b.t.insertOne({ i: i, x: 'dato-' + i }, { writeConcern: { w: 1 } }); });
b.t.drop();
let tj = 'no aplica (sin journal)';
try { tj = t(() => { for (let i = 0; i < N; i++) b.t.insertOne({ i: i, x: 'dato-' + i }, { writeConcern: { w: 1, j: true } }); }); } catch (e) { tj = 'error: ' + e.message; }
b.t.drop();
const docs = []; for (let i = 0; i < 400000; i++) docs.push({ i: i, pais: i % 8, x: 'dato-' + i });
const tm = t(() => { for (let k = 0; k < docs.length; k += 10000) b.t.insertMany(docs.slice(k, k + 10000), { ordered: false }); });
const tsc = t(() => b.t.find({ x: 'dato-399999' }).toArray());
const tagg = t(() => b.t.aggregate([{ $group: { _id: '$pais', n: { $sum: 1 } } }]).toArray());
print(JSON.stringify({ motor: motor, insertOne_w1_5000_ms: tw, insertOne_j_true_5000_ms: tj, insertMany_400000_ms: tm, scan_400000_ms: tsc, aggregate_group_400000_ms: tagg }));
