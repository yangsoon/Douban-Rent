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
