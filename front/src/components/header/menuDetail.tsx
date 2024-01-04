import React, {useState} from "react";
import styled from "styled-components";
import ListBox from "./clubBox";
import club from "../../static/data/club.json"
import {SelectBox} from "../selectBox/selectBox"
import {SubmitHandler} from "../../handler/handler";
import {departure, destination, navResult} from "./searchingMenu/store";

function SearchingMenu() {
    const [departureValue, setDeparture] = useState('');
    const [destinationValue, setDestination] = useState('');
    const getDeparture = (departure: string) => {
        setDeparture(departure)
    }
    const getDestination = (destination: string) => {
        setDestination(destination)
    }

    function getSubmit(){
        console.log(SubmitHandler(departureValue, destinationValue));
    }
    return(
        <MenuArea>
            <StartpointArea>
                <SelectBox placeholder={"출발지를 입력하세요"} getValue={getDeparture}></SelectBox>
            </StartpointArea>
            <EndpointArea>
                <SelectBox placeholder={"도착지를 입력하세요"} getValue={getDestination}></SelectBox>
            </EndpointArea>

            <FindingWayBox onClick={() => getSubmit()}>길찾기</FindingWayBox>
        </MenuArea>
    )
}

function ClubMenu(){
    return(
        <ClubArea>
            {/*<ListBox margin-top={"16px"}></ListBox>*/}
            {club.map((data: any) => {
                return <ListBox name={data.name} description={data.description}></ListBox>
            })}
        </ClubArea>
    )
}

export {SearchingMenu, ClubMenu};

const MenuArea = styled.div`
  width: 366px;
  height: 260px;
`

const StartpointArea = styled.div`
  position: absolute;
  top: 18px;
  left: 35px;
`

const EndpointArea = styled.div`
  position: absolute;
  top: 83px;
  left: 35px;
`

const FindingWayBox = styled.div`
  position: absolute;
  left: 35px;
  Top: 151px;
  width: 297px;
  height: 40px;
  border: none;
  border-radius: 10px;
  background-color: #9CA6FF;
  color: #FFFFFF;
  cursor: pointer;
  font-size: medium;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
`

const ClubArea = styled.div`
  width: 366px;
  margin-top: 16px;
  display: flex;
  align-items: center;
  flex-direction: column;
`
