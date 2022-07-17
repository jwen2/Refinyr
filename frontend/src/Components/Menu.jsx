import axios from "axios";
import React, { useState } from "react";
import { NavDropdown, Navbar, Nav } from "react-bootstrap";
import { DropdownSubmenu, NavDropdownMenu } from "react-bootstrap-submenu";
import "./Menu.css";
import { useEffect } from "react";

const Menu = ({
  fileSelected,
  filename,
  columnSelected,
  setColumnDefs,
  setRowData,
  setDataTypes,
  attribute,
  currentType,
}) => {
  // useEffect(() => {
  //   if (filename && columnSelected && selection) {
  //     handleClick(selection);
  //   }
  // }, [selection, filename]);

  const handleSelect = (val) => {
    handleClick(val);
  };

  const handleClick = async (selection) => {
    try {
      const { data } = await axios.get(
        `http://127.0.0.1:5000/pandas/${selection}/${filename}/${columnSelected}`,
        filename,
        columnSelected
      );
      console.log(data);
      setRowData(data[0]);
      console.log(data[0][0]);

      let keys = Object.keys(data[0][0]).map((key) => ({
        field: key,
        headerName: key[0].toUpperCase() + key.slice(1),
        editable: true,
        // sortable: true,
        resizable: true,
        cellStyle: (params) => {
          if (params.colDef.field === attribute) {
            return { color: "#001D6D", backgroundColor: "#F3F7FF" };
          }
          return null;
        },
      }));
      keys.forEach((key, i) => {
        key["columnType"] = data[1][i];
      });
      setDataTypes(data[1]);
      console.log(data[1]);
      console.log(keys);
      setColumnDefs(keys);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <>
      <div className="optionsContainer">
        <p className="typeFont">Column Type: {currentType}</p>
        {currentType === "int64" ? (
          <Navbar
            collapseOnSelect
            bg="dark"
            variant="dark"
            style={{ height: "2.5vh", marginBottom: "1.2em" }}
          >
            <Navbar.Toggle aria-controls="responsive-navbar-nav" />
            <Navbar.Collapse id="responsive-navbar-nav">
              <Nav className="mr-auto">
                <NavDropdownMenu
                  title="Transform"
                  id="collasible-nav-dropdown"
                  alignRight
                >
                  <DropdownSubmenu title="Treating Nulls">
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
                  <DropdownSubmenu title="Transformations">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("normalize");
                      }}
                    >
                      Normalize
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("transformer_squared");
                      }}
                    >
                      <var>
                        X<sup>2</sup>
                      </var>
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("transformer_log");
                      }}
                    >
                      ln(x)
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("transformer_root2");
                      }}
                    >
                      Square Root
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("quartile_trimmer");
                      }}
                    >
                      Trim Quantiles
                    </NavDropdown.Item>
                  </DropdownSubmenu>

                  <DropdownSubmenu title="Treating Outliers">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("");
                      }}
                    >
                      Remove outliers
                    </NavDropdown.Item>
                  </DropdownSubmenu>

                  <DropdownSubmenu title="Change Data Type">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("change_data_type_to_date");
                      }}
                    >
                      Numeric to Date
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("change_data_type_int_to_cat");
                      }}
                    >
                      Numeric to Categorical
                    </NavDropdown.Item>
                  </DropdownSubmenu>

                  <DropdownSubmenu title="Rename">
                    <NavDropdown.Item>Sub 2</NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu title="Find and Replace">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("");
                      }}
                    >
                      Sub 2
                    </NavDropdown.Item>
                    {() => {
                      handleSelect("");
                    }}
                  </DropdownSubmenu>
                </NavDropdownMenu>
              </Nav>
            </Navbar.Collapse>
          </Navbar>
        ) : (
          ""
        )}

        {currentType === "float64" ? (
          <Navbar
            collapseOnSelect
            bg="dark"
            variant="dark"
            style={{ height: "2.5vh", marginBottom: "1.2em" }}
          >
            <Navbar.Toggle aria-controls="responsive-navbar-nav" />
            <Navbar.Collapse id="responsive-navbar-nav">
              <Nav className="mr-auto">
                <NavDropdownMenu
                  title="Transform"
                  id="collasible-nav-dropdown"
                  alignRight
                >
                  <DropdownSubmenu title="Treating Nulls">
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
                  <DropdownSubmenu title="Transformations">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("normalize");
                      }}
                    >
                      Normalize
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("transformer_squared");
                      }}
                    >
                      <var>
                        X<sup>2</sup>
                      </var>
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("transformer_log");
                      }}
                    >
                      ln(x)
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("transformer_root2");
                      }}
                    >
                      Square Root
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("quartile_trimmer");
                      }}
                    >
                      Trim Quantiles
                    </NavDropdown.Item>
                  </DropdownSubmenu>

                  <DropdownSubmenu title="Treating Outliers">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("");
                      }}
                    >
                      Remove outliers
                    </NavDropdown.Item>
                  </DropdownSubmenu>

                  <DropdownSubmenu title="Change Data Type">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("change_data_type_to_date");
                      }}
                    >
                      Numeric to Date
                    </NavDropdown.Item>
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("change_data_type_int_to_cat");
                      }}
                    >
                      Numeric to Categorical
                    </NavDropdown.Item>
                  </DropdownSubmenu>

                  <DropdownSubmenu title="Rename">
                    <NavDropdown.Item>Sub 2</NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu title="Find and Replace">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("");
                      }}
                    >
                      Sub 2
                    </NavDropdown.Item>
                    {() => {
                      handleSelect("");
                    }}
                  </DropdownSubmenu>
                </NavDropdownMenu>
              </Nav>
            </Navbar.Collapse>
          </Navbar>
        ) : (
          ""
        )}

        {currentType === "object" ? (
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
                  title="Transform"
                  id="collasible-nav-dropdown"
                  alignRight
                >
                  <DropdownSubmenu title="Treating Nulls">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("rm_nulls");
                      }}
                    >
                      Remove nulls
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

                  <DropdownSubmenu title="Transformations">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("get_dummies");
                      }}
                    >
                      Create Dummy Variable
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                  <DropdownSubmenu href="#action/3.7" title="Change Data Type">
                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("change_data_type_to_date");
                      }}
                    >
                      Categorical to Date
                    </NavDropdown.Item>

                    <NavDropdown.Item
                      onClick={() => {
                        handleSelect("change_data_type_cat_to_int");
                      }}
                    >
                      Categorical to Numeric
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
                        handleSelect("");
                      }}
                    >
                      Sub 2
                    </NavDropdown.Item>
                  </DropdownSubmenu>
                </NavDropdownMenu>
              </Nav>
            </Navbar.Collapse>
          </Navbar>
        ) : (
          ""
        )}
      </div>
    </>
  );
};
export default Menu;
