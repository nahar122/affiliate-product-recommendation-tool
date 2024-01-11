import { ChangeEvent, FormEvent, useState } from "react";
import { signInUser } from "../firebase/firebase";
import { useNavigate } from "react-router-dom";

const defaultFormFields = {
  email: "",
  password: "",
};

function SignIn() {
  const [formFields, setFormFields] = useState(defaultFormFields);
  const { email, password } = formFields;
  const navigate = useNavigate();

  const resetFormFields = () => {
    return setFormFields(defaultFormFields);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      // Send the email and password to firebase
      const userCredential = await signInUser(email, password);

      if (userCredential) {
        resetFormFields();
        navigate("/");
      }
    } catch (error: any) {
      console.log("User Sign In Failed", error.message);
    }
  };

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormFields({ ...formFields, [name]: value });
  };

  return (
    <div className="App w-1/2 mt-40 flex flex-col justify-center mx-auto border border-neutral rounded-md">
      <h1 className="text-xl font-semibold mx-auto text-center p-4">Login</h1>
      <div className="card p-10">
        <form className="w-full" onSubmit={handleSubmit}>
          <label className="flex w-full align-middle items-center justify-between p-2">
            <span className="w-1/2">Email:</span>
            <div className="w-1/2">
              <input
                className="input input-bordered focus:border-none active:border-none w-full"
                name="email"
                onChange={(e) => handleChange(e)}
              />
            </div>
          </label>
          <label className="flex w-full align-middle items-center justify-between p-2">
            <span className="w-1/2">Password:</span>
            <div className="w-1/2">
              <input
                className="input input-bordered w-full"
                name="password"
                type="password"
                onChange={(e) => handleChange(e)}
              />
            </div>
          </label>

          <button
            type="submit"
            className="btn btn-neutral text-white p-4 mt-5 w-full"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  );
}

export default SignIn;
