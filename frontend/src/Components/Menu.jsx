import axios from "axios";
import React, { useState } from "react";
import Select from "react-select";
import { NavDropdown, Navbar, Nav, Row } from "react-bootstrap";
import { DropdownSubmenu, NavDropdownMenu } from "react-bootstrap-submenu";
import "./Menu.css";
import { useEffect } from "react";

const Menu = ({
  fileSelected,
  filename,
  columnSelected,
  setColumnDefs,
  setRowData,
}) => {
  const [selection, setSelection] = useState("");

  //can be replaced dynamic data with an async call
  const options = [
    { value: "rm_dups", label: "Remove Duplicates" },
    { value: "rm_nulls", label: "Remove Nulls" },
    { value: "replace_na_mean", label: "Replace NA with Mean" },
    { value: "replace_na_median", label: "Replace NA with Median" },
    { value: "replace_na_mode_numeric", label: "Replace NA with Mode Numeric" },
    { value: "replace_na_unknown", label: "Replace NA with Unknown" },
    { value: "replace_na_ffill", label: "Replace NA with ffill" },
    { value: "replace_na_bfill", label: "Replace NA with bfill" },
    {
      value: "replace_na_mode_categorical",
      label: "Replace NA with Mode Categorical",
    },
    //need to have pop up or something to input second value for rename column
    //{ value: "rename_column", label: "Rename Column"},
    { value: "normalize", label: "Normalize Column" },
  ];

  useEffect(() => {
    if (filename && columnSelected && selection) {
      handleClick(selection);
    }
  }, [selection]);

  const handleSelect = (val) => {
    setSelection(val);
  };

  const handleClick = async () => {
    console.log(filename);
    console.log(columnSelected);
    console.log(selection);
    try {
      const res = await axios.get(
        `http://127.0.0.1:5000/pandas/${selection}/${filename}/${columnSelected}`,
        filename,
        columnSelected
      );
      console.log(res.data);
      setRowData(res.data);

      const keys = Object.keys(res.data[0]).map((key) => ({
        field: key,
        headerName: key[0].toUpperCase() + key.slice(1),
      }));
      setColumnDefs(keys);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <div className="optionsContainer">
        <p>Transform:</p>

        <Navbar
          collapseOnSelect
          bg="dark"
          variant="dark"
          style={{ height: "3vh" }}
        >
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="mr-auto">
              <NavDropdownMenu
                title="Options"
                id="collasible-nav-dropdown"
                alignRight
              >
                {/* Numeric */}
                <DropdownSubmenu href="#action/3.7" title="Numeric">
                  <DropdownSubmenu href="#action/3.7" title="Treating Nulls">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_nulls");
                      }}
                    >
                      Remove nulls
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("replace_na_mean");
                      }}
                    >
                      Replace with mean
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("replace_na_median");
                      }}
                    >
                      Replace with median
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("replace_na_mode_numeric");
                      }}
                    >
                      Replace with mode
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("replace_na_ffill");
                      }}
                    >
                      Replace with forward fill
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("replace_na_bfill");
                      }}
                    >
                      Replace with back fill
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu title="Treating Duplicates">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Remove duplicates
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu href="#action/3.7" title="Transformations">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_nulls");
                      }}
                    >
                      Normalize
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_nulls");
                      }}
                    >
                      <var>
                        X<sup>2</sup>
                      </var>
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_nulls");
                      }}
                    >
                      ln(x)
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_nulls");
                      }}
                    >
                      Square Root
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_nulls");
                      }}
                    >
                      Trim Quantiles
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu href="#action/3.7" title="Treating Outliers">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_nulls");
                      }}
                    >
                      Remove outliers
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu href="#action/3.7" title="Rename">
                    <NavDropdown.Item href="#action/9.1">
                      Sub 2
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu href="#action/3.7" title="Find and Replace">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_nulls");
                      }}
                    >
                      Sub 2
                    </NavDropdown.Item>
                    onClick=
                    {() => {
                      handleSelect("rm_nulls");
                    }}
                  </DropdownSubmenu>
                </DropdownSubmenu>

                {/* Categorical */}
                <DropdownSubmenu href="#action/3.7" title="Categorical">
                  <DropdownSubmenu href="#action/3.7" title="Treating Nulls">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_nulls");
                      }}
                    >
                      Remove nulls
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_nulls");
                      }}
                    >
                      Replace with mode
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_nulls");
                      }}
                    >
                      Replace with forward fill
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_nulls");
                      }}
                    >
                      Replace with back fill
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu
                    href="#action/3.7"
                    title="Treating Duplicates"
                  >
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Treating duplicates
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu href="#action/3.7" title="Transformations">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Create Dummy Variable
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu href="#action/3.7" title="Rename">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Sub 2
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu href="#action/3.7" title="Find and Replace">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Sub 2
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                </DropdownSubmenu>

                {/* Date */}
                <DropdownSubmenu href="#action/3.7" title="Date">
                  <DropdownSubmenu href="#action/3.7" title="Treating Nulls">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Remove nulls
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Replace with mode
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Replace with forwad fill
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Replace with back fill
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu
                    href="#action/3.7"
                    title="Treating Duplicates"
                  >
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Remove duplicates
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu href="#action/3.7" title="Transformations">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Extract Day
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Extract Month
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Extract Year
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Extract Quarter
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Extract Year
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Extract Quarter
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Extract Day of Week (Int)
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Extract Day of Week (Day Name)
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu href="#action/3.7" title="Rename">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Sub 2
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu href="#action/3.7" title="Find and Replace">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Sub 2
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                </DropdownSubmenu>

                {/* Text */}

                <DropdownSubmenu href="#action/3.7" title="Text">
                  <DropdownSubmenu href="#action/3.7" title="Treating Nulls">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Sub 2
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu
                    href="#action/3.7"
                    title="Treating Duplicates"
                  >
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Sub 2
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu href="#action/3.7" title="Transformations">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Sub 2
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu href="#action/3.7" title="Rename">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Sub 2
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu href="#action/3.7" title="Find and Replace">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_dups");
                      }}
                    >
                      Sub 2
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                </DropdownSubmenu>
              </NavDropdownMenu>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
      </div>
    </>
  );
};
export default Menu;
