import axios from "axios"

let baseURL = 'https://43.251.228.66:8080';

const instance = axios.create({
  baseURL: baseURL
});

let ajax = {

};

ajax.getPlace = function () {
  return instance.get("/placelists")
};

ajax.getRent = function (params) {
  return instance.get("/getrent", {
    params
  })
};

ajax.getDetail = function (params) {
  return instance.get("/getdetail", {
    params
  })
};

ajax.filterRent = function (params) {
  return instance.get("/filterrent", {
    params
  })
};

export default ajax;
