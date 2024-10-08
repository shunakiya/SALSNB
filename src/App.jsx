import { LockKeyhole, Mail, DoorOpen } from "lucide-react";
import { useState } from "react";
import googleIcon from "./assets/google.svg";
import appleIcon from "./assets/apple.svg";

export default function App() {
  const [test, setData] = useState(null);

  const testFetch = async () => {
    try {
      const response = await fetch(`http://192.168.137.221:5000`);
      const data = await response.json();
      setData(data);
    } catch (error) {
      console.log("Error fetching data:", error);
    }
  };

  const bg = "https://i.imgur.com/qlXKnfB.png";

  return (
    <div className="relative min-h-screen overflow-hidden">
      <div
        className="absolute inset-0 bg-cover overflow-hidden"
        style={{
          backgroundImage: `url(${bg})`,
          filter: "blur(2px)",
          transform: "scale(1.1)",
        }}
      />

      <div className="relative z-10 flex items-center justify-center min-h-screen p-4">
        <div className="bg-white/50 backdrop-blur-md p-7 rounded-2xl shadow-2xl drop-shadow-xl w-96">
          <div className="mb-4">
            <div className="flex justify-center mb-4">
              <div className="rounded-lg shadow-2xl drop-shadow-xl border-transparent w-min p-3 bg-slate-200">
                <DoorOpen />
              </div>
            </div>

            <header className="text-2xl font-semibold text-center mb-2">
              iOpen
            </header>

            <p className="text-gray-500 text-center w-64  mx-auto text-sm">
              Experience effortless access, and unlock your world with a tap or
              touch.
            </p>
          </div>

          <div className="flex flex-col w-full gap-y-4">
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 h-5 w-5" />
              <input
                type="text"
                placeholder="Email"
                className="w-full pl-10 pr-3 py-3 bg-[#EFF2F6] text-sm placeholder-gray-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
              />
            </div>

            <div className="relative">
              <LockKeyhole className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 h-5 w-5" />
              <input
                type="password"
                placeholder="Password"
                className="w-full pl-10 pr-3 py-3 bg-[#EFF2F6] text-sm placeholder-gray-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
              />
            </div>
          </div>

          <div className="justify-center items-center text-center mt-4">
            <button className="w-full bg-blue-600 text-white font-semibold rounded-lg py-2 transition-opacity duration-175 ease-in-out hover:opacity-85 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
              Login
            </button>

            <div className="flex flex-row gap-x-2 text-center justify-center mt-4 mb-4">
              <p className="text-xs text-white/30">
                • • • • • • • • • • • • • • •
              </p>
              <p className="text-xs text-gray-500">Or sign in with</p>
              <p className="text-xs text-white/30">
                • • • • • • • • • • • • • •
              </p>
            </div>

            <div className="w-full justify-center flex gap-x-2">
              <button className=" bg-white rounded-xl shadow-md border px-8 py-2 transition-opacity duration-175 ease-in-out hover:opacity-85 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
                <img src={googleIcon} className="w-5" />
              </button>

              <button className=" bg-white rounded-xl shadow-md border px-8 py-2 transition-opacity duration-175 ease-in-out hover:opacity-85 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
                <img src={appleIcon} className="w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
