const app = {
  state :{
    place: null,
    idx: null,
    rent: null,
  },
  mutations:{
    setPlace(state, params){
      state.place = params['place'];
      state.idx = params['idx']
    },
    setRent(state, rent){
      state.rent = rent
    }
  }
};
export default app;
