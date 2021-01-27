import axios from "axios";
import jsSHA from "jssha";

const baseUrl = "http://localhost:5000/user";
const config = {
    dataType: "json",
    headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
    },
};

export default {
    getAllUsers() {
        console.log("Getting all users");
        return axios.get(baseUrl, config);
    },
    addUser(user) {
        const sha256 = new jsSHA("SHA-256", "TEXT", { encoding: "UTF8" });
        sha256.update(user.password);
        user.password = sha256.getHash("B64");

        console.log("Saving user");
        console.log(user);
        return axios.post(baseUrl, user, config);
    },
    updateUser(user) {
        const sha256 = new jsSHA("SHA-256", "TEXT", { encoding: "UTF8" });
        sha256.update(user.password);
        user.password = sha256.getHash("B64");

        console.log("Saving user");
        console.log(user);
        return axios.put(baseUrl, user, config);
    },
    deleteUser(id) {
        const url = `${baseUrl}/${id}`;
        return axios.delete(url, config);
    }
};
