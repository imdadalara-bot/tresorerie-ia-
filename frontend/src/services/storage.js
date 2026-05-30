const DB_NAME = 'tresorier_ia';
const DB_VERSION = 1;

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains('transactions')) {
        const store = db.createObjectStore('transactions', { keyPath: 'id' });
        store.createIndex('date', 'date', { unique: false });
        store.createIndex('synced', 'synced', { unique: false });
      }
      if (!db.objectStoreNames.contains('dashboard')) {
        db.createObjectStore('dashboard', { keyPath: 'key' });
      }
    };

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

export const offlineStorage = {
  async saveTransaction(txn) {
    const db = await openDB();
    const tx = db.transaction('transactions', 'readwrite');
    tx.objectStore('transactions').put({ ...txn, synced: false });
    return new Promise((resolve, reject) => {
      tx.oncomplete = resolve;
      tx.onerror = () => reject(tx.error);
    });
  },

  async getUnsyncedTransactions() {
    const db = await openDB();
    const tx = db.transaction('transactions', 'readonly');
    const index = tx.objectStore('transactions').index('synced');
    const request = index.getAll(false);
    return new Promise((resolve, reject) => {
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  },

  async markSynced(id) {
    const db = await openDB();
    const tx = db.transaction('transactions', 'readwrite');
    const store = tx.objectStore('transactions');
    const request = store.get(id);
    request.onsuccess = () => {
      const record = request.result;
      if (record) {
        record.synced = true;
        store.put(record);
      }
    };
  },

  async cacheDashboard(data) {
    const db = await openDB();
    const tx = db.transaction('dashboard', 'readwrite');
    tx.objectStore('dashboard').put({ key: 'latest', ...data, cachedAt: Date.now() });
  },

  async getCachedDashboard() {
    const db = await openDB();
    const tx = db.transaction('dashboard', 'readonly');
    const request = tx.objectStore('dashboard').get('latest');
    return new Promise((resolve) => {
      request.onsuccess = () => resolve(request.result || null);
      request.onerror = () => resolve(null);
    });
  },
};
