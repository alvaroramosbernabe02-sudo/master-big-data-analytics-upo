printjson(db.articles.aggregate(
  [
    { $group: { _id: "$contributorusername", count: { $sum: 1 } } },
    { $sort: { count: -1 } },
    { $limit: 10 }
  ]
).toArray())
