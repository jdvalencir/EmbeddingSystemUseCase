"use client";

import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  Navbar,
  NavbarBrand,
  NavbarMenuToggle,
  NavbarMenu,
  NavbarMenuItem,
  NavbarContent,
  NavbarItem,
  Link,
  Button,
  Chip,
  Input,
} from "@heroui/react";
import Image from "next/image";
import { useCallback, useState } from "react";

export default function Home() {
  interface DataItem {
    key: string;
    text: string;
    similarity: number;
  }

  interface Response {
    query: string;
    results: DataItem[];
  }

  const [data, setData] = useState<Response>();
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [error, setError] = useState<String>("");

  const PostFetch = async () => {
    if (!search) {
      return;
    }
    try {
      const response = await fetch("http://localhost:8000/search/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: search,
        }),
      });
      const data = await response.json();

      setData(data);
    } catch (error: any) {
      setError(error);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { key: "key", label: "Key" },
    { key: "date", label: "Date" },
    { key: "text", label: "Log" },
    { key: "similarity", label: "Similarity" },
  ];

  const renderCell = useCallback((dataItem: DataItem, columnKey: string) => {
    const cellValue = dataItem[columnKey as keyof DataItem];

    switch (columnKey) {
      case "key":
        return <Chip color="danger">{cellValue}</Chip>;
      case "date":
        return <p>{new Date(cellValue).toLocaleString()}</p>;
      case "text":
        return <p>{cellValue}</p>;
      case "similarity":
        return <Chip>{(Number(cellValue) * 100).toFixed(2) + "%"}</Chip>;
      default:
        return cellValue;
    }
  }, []);

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <>
      <Navbar disableAnimation isBordered>
        <NavbarContent className="sm:hidden" justify="start">
          <NavbarMenuToggle />
        </NavbarContent>

        <NavbarContent className="sm:hidden pr-3" justify="center">
          <NavbarBrand>
            <p className="">Piano Embrujado</p>
          </NavbarBrand>
        </NavbarContent>
        <NavbarContent justify="center">
          <NavbarBrand className="flex gap-3">
            <Image
              alt="Logo"
              className="rounded-full"
              height={40}
              src="/logo.png"
              width={40}
            />
            <p className="text-xl font-bold">Piano Embrujado</p>
          </NavbarBrand>
        </NavbarContent>
      </Navbar>
      <div className="flex flex-col justify-center items-center w-full flex-wrap md:flex-nowrap gap-4 p-10 ">
        <div className="flex w-2/5 flex-col gap-4">
          <h1 className="flex justify-center text-2xl">Search Logs:</h1>
          <Input
            label="Input"
            type="text"
            onChange={(e) => {
              setSearch(e.target.value);
            }}
          />
          <div className="flex justify-center gap-4">
            <Button className="w-32" color="primary" onPress={PostFetch}>
              Search
            </Button>
            <Button
              className="w-32"
              color="danger"
              onPress={() => setLoading(true)}
            >
              Clear
            </Button>
          </div>
        </div>

        {!loading && (
          <>
            <div className="w-4/5">
              <h1 className="flex text-2xl w-4/5">Results:</h1>
            </div>
            <Table aria-label="Simple Table" className="w-4/5">
              <TableHeader columns={columns}>
                {(column) => (
                  <TableColumn key={column.key}>{column.label}</TableColumn>
                )}
              </TableHeader>
              <TableBody items={data?.results}>
                {(item) => (
                  <TableRow key={item.key}>
                    {(columnKey) => (
                      <TableCell>
                        {renderCell(item, String(columnKey))}
                      </TableCell>
                    )}
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </>
        )}
      </div>
    </>
  );
}
