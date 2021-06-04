import React, { useEffect, useState } from "react";
import { BsTrashFill, BsPencilSquare } from "react-icons/bs";

const ControlledInputs = () => {
  const [firstName, setFirstName] = useState("");
  const [age, setAge] = useState("");
  const [people, setPeople] = useState([]);
  const [upload, setUpload] = useState([]);
  const [showAlert, setShowAlert] = useState(false);
  const [alert, setAlert] = useState("");
  const [alertMessage, setAlertMessage] = useState("");
  const [updateData, setUpdateData] = useState({
    isUpdate: false,
    filters: {},
  });
  const [download_path, setDownloadPath] = useState("");
  const insert_pattern = {
    tablename: "test",
    columns: { id: "", name: "", age: "" },
    filter: {},
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    if (firstName && age) {
      const data = [people.length, firstName, age];

      setUpload((upload) => {
        return [...upload, data];
      });
      if (updateData["isUpdate"]) {
        if (
          updateData["filters"]["name"] === firstName &&
          updateData["filters"]["age"] === age
        ) {
          handleAlert(true, "danger", "Please make change to update data");
        } else {
          const update_details = {
            ...insert_pattern,
            filters: updateData["filters"],
            update: { id: people.length, name: firstName, age: age },
          };
          handleUpload("update", update_details);
          setUpdateData({ ...updateData, isUpdate: false });
          setFirstName("");
          setAge("");
        }
      } else {
        handleUpload("insert", {
          ...insert_pattern,
          columns: { id: people.length, name: firstName, age: age },
        });
        console.log(people);
        setFirstName("");
        setAge("");
      }
    } else {
      console.log("empty values");
    }
  };

  const get_all_data = (type) => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      "Access-Control-Allow-Origin": "*",
      body: JSON.stringify({
        tablename: "test",
        columns: ["id", "name", "age"],
        filters: {},
      }),
    };
    const fromDb = fetch(`http://127.0.0.1:5000/${type}`, requestOptions)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);

        if (type === "select") {
          if (data["data"].length > 0) {
            const newData = data["data"].map((d) => {
              return { id: d[0], firstName: d[1], age: d[2] };
            });
            setPeople(newData);
          }
        } else if (type == "download") {
          console.log(data);
          if (data.hasOwnProperty("file_name")) {
            setDownloadPath(data["file_name"]);
          }
          // if (data["status"] == "success") {
          //   handleAlert(true, "success", data["message"]);
          // } else {
          //   handleAlert(true, "danger", data["message"]);
          // }
        }
      })
      .catch((err) => console.log(err));
    console.log(fromDb);
  };

  const get_data = () => {
    get_all_data("select");
    get_all_data("download");
  };
  useEffect(() => {
    get_data();
  }, []);

  const handleUpload = (datatype, data) => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      "Access-Control-Allow-Origin": "*",
      body: JSON.stringify(data),
    };
    fetch(`http://127.0.0.1:5000/${datatype}`, requestOptions)
      .then((response) => response.json())
      .then((data) => {
        handleAlert(true, "success", data["message"]);
      })
      .then(() => get_data())
      .catch((err) => {
        console.log(err);
        handleAlert(
          true,
          "danger",
          "something went wrong.. Please try again later"
        );
      });
  };
  const handleDelete = (data) => {
    handleUpload("delete", { ...insert_pattern, columns: {}, filters: data });
  };

  const handleEdit = (data) => {
    setUpdateData({ isUpdate: true, filters: data });
    setFirstName(data["name"]);
    setAge(data["age"]);
  };

  const handleAlert = (show, type, msg) => {
    setShowAlert(show);
    setAlert(type);
    setAlertMessage(msg);
  };
  useEffect(() => {
    const disableAlert = setInterval(() => {
      setShowAlert(false);
    }, 3000);
    return () => {
      clearInterval(disableAlert);
    };
  }, [showAlert]);
  return (
    <>
      <article>
        {showAlert && (
          <div className="alert">
            <div className={`alert-${alert}`}>{alertMessage}</div>
          </div>
        )}

        <form className="form" onSubmit={handleSubmit}>
          <div className="form-control">
            <label htmlFor="firstName">Name : </label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
            />
          </div>
          <div className="form-control">
            <label htmlFor="email">Age : </label>
            <input
              type="number"
              id="email"
              name="email"
              value={age}
              onChange={(e) => setAge(e.target.value)}
            />
          </div>
          <button type="submit">
            {updateData["isUpdate"] ? "update " : "add person"}
          </button>
        </form>
        {people.map((person, index) => {
          const { id, firstName, age } = person;
          return (
            <div className="item" key={index}>
              <h4>{firstName}</h4>
              <p>{age}</p>

              <div className="btn-container">
                <BsPencilSquare
                  className="edit-btn"
                  onClick={() => handleEdit({ name: firstName, age: age })}
                />
                <BsTrashFill
                  className="delete-btn"
                  onClick={() => handleDelete({ name: firstName, age: age })}
                />
              </div>
            </div>
          );
        })}
        <a
          href={"http://127.0.0.1:5000/download_data/" + download_path}
          download
        >
          Click here to download data
        </a>
      </article>
    </>
  );
};

export default ControlledInputs;
