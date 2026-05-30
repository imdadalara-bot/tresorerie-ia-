import { writable, derived } from 'svelte/store';

function createUserStore() {
  const stored = typeof localStorage !== 'undefined' ? localStorage.getItem('user') : null;
  const initial = stored ? JSON.parse(stored) : null;
  const { subscribe, set, update } = writable(initial);

  return {
    subscribe,
    set: (value) => {
      if (value) {
        localStorage.setItem('user', JSON.stringify(value));
      } else {
        localStorage.removeItem('user');
      }
      set(value);
    },
    update,
  };
}

export const user = createUserStore();
export const isAuthenticated = derived(user, ($user) => !!$user);
