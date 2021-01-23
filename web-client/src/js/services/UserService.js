import axios from "axios";

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
    getUser(id) {
        console.log("Getting user");
        const url = `${baseUrl}/${id}`;
        return axios.get(url, config);
    },
    getUserAuthorization(id) {
        console.log("Getting user authorization");
        const url = `${baseUrl}/${id}/authorized`;
        return axios.get(url, config);
    },
    addUser(user) {
        console.log("Saving user");
        console.log(user);
        return axios.post(baseUrl, user, config);
    },
    updateUser(user) {
        console.log("Saving user");
        console.log(user);
        return axios.put(baseUrl, user, config);
    },
    deleteUser(id) {
        const url = `${baseUrl}/${id}`;
        return axios.delete(url, config);
    }
};
