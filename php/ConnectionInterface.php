<?php
/**
 * Created by PhpStorm.
 * User: jonse
 * Date: 16.10.2017
 * Time: 15:58
 */

interface ConnectionInterface
{
    public function receiveLength(int $length);

    public function receive();

    public function sendallBytes();

    public function sendallString(string $string);

    public function sendString(string $string);

    public function sendJSON(object $obj);

    public function send(object $obj);
}