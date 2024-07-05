// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import{getAuth} from "firebase/auth";


const firebaseConfig = {
  apiKey: "AIzaSyDQ1ri5_NRVKRw1pvxR86eDSpRNU5QDjB0",
  authDomain: "fir-183ac.firebaseapp.com",
  projectId: "fir-183ac",
  storageBucket: "fir-183ac.appspot.com",
  messagingSenderId: "425969052179",
  appId: "1:425969052179:web:a205c3e0b78127a07b6de6"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export default app;