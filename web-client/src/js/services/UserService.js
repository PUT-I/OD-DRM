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
