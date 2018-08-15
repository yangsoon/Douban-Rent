const app = {
  state :{
      place: null,
      idx: null,
      rent: null,
      loading: false,
      number: null,
      current: 1
  },
  mutations:{
      setPlace(state, params){
        state.place = params['place'];
        state.idx = params['idx']
      },
      setRent(state, rent){
        state.rent = rent
      },
      setLoading(state, loading){
        state.loading = loading
      },
      setNumber(state, number){
        state.number = number
      },
      setCurrent(state, current){
        state.current = current
      }
  }
};
export default app;
