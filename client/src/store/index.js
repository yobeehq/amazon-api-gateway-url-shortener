import { createStore } from 'vuex'

export default createStore({
  state() {
    return {
      authorized: false,
      links: []
    }
  },
  mutations: {
    authorize(state) {
      state.authorized = true;
    },
    deAuthorize(state) {
      state.authorized = false;
    },
    hydrateLinks(state, links) {
      state.links = links;
    },
    drainLinks(state) {
      state.links = [];
    },
    addLink(state, link) {
      state.links.push(link);
    },
    removeLink(state, ind) {
      state.links.splice(ind, 1);
    },
    updateLink(state, { link, ind }) {
      state.links[ind] = link;
    }
  }
})