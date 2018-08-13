import axios from "axios"

let baseURL = 'http://localhost:8888';

const instance = axios.create({
  baseURL: baseURL
});

let ajax = {

};

ajax.getPlace = function () {
  return instance.get("/placelists")
};

export default ajax;
