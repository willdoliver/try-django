var db = connect("mongodb://localhost/admin");

db.createUser(
    {
        user: "root",
        pwd: "pass",
        roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
    }
)
