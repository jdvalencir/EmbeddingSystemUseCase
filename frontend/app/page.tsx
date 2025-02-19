"use client";

import { Chip, getKeyValue, Input } from "@heroui/react";
import { Button } from "@heroui/react";
import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
} from "@heroui/react";
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

  const PostFetch = async () => {
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
      console.log(data);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
      console.log("done");
    }
  };

  const columns = [
    { key: "key", label: "Key" },
    { key: "text", label: "Text" },
    { key: "similarity", label: "Similitud" },
  ];

  const renderCell = useCallback((dataItem: DataItem, columnKey: string) => {
    const cellValue = dataItem[columnKey as keyof DataItem];

    switch (columnKey) {
      case "key":
        return <Chip color="danger">{cellValue}</Chip>;
      case "text":
        return <p>{cellValue}</p>;
      case "similarity":
        return <Chip>{(Number(cellValue) * 100).toFixed(2) + "%"}</Chip>;
      default:
        return cellValue;
    }
  }, []);

  return (
    <div className="flex flex-col justify-center items-center w-full h-screen flex-wrap md:flex-nowrap gap-4 py-10">
      <div className="flex w-2/5 flex-col gap-4">
        <h1 className="flex justify-center text-2xl">Search Logs:</h1>
        <Input
          label="Input"
          type="text"
          onChange={(e) => {
            setSearch(e.target.value);
          }}
        />
        <div className="flex justify-center">
          <Button color="primary" className="w-32" onPress={PostFetch}>
            Button
          </Button>
        </div>
      </div>

      {!loading && (
        <>
          <h1 className="flex text-2xl w-4/5">Results:</h1>
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
                    <TableCell>{renderCell(item, String(columnKey))}</TableCell>
                  )}
                </TableRow>
              )}
            </TableBody>
          </Table>
        </>
      )}
    </div>
  );
}
